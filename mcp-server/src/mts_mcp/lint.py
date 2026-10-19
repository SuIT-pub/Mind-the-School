from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# Person characters are created at runtime, so lint cannot evaluate them and
# reports every one of their say statements. That is ~1700 lines of noise per
# run; we fold them into a per-name count so a typo ('emkio') still shows up.
_SAY_WHO_RE = re.compile(r"Could not evaluate '([^']+)' in the who part of a say statement\.")
_ISSUE_RE = re.compile(r"^(game/\S+?):(\d+) ")


@dataclass(frozen=True, slots=True)
class LintIssue:
    file: str
    line: int
    text: str


@dataclass(slots=True)
class LintReport:
    issues: list[LintIssue] = field(default_factory=list)
    say_who_counts: Counter[str] = field(default_factory=Counter)
    other_blocks: list[str] = field(default_factory=list)


def parse_lint_report(text: str) -> LintReport:
    """Split a Ren'Py lint report into real issues and folded say-who noise.

    The report is blank-line separated blocks. Everything from "Statistics:"
    on is dialogue counts, not findings, and is dropped.
    """
    report = LintReport()
    # Ren'Py writes the report with a UTF-8 BOM, which would hide the header from the check below.
    body = text.lstrip("﻿").split("\nStatistics:", 1)[0]
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or block.startswith("Ren'Py ") and "lint report" in block:
            continue
        match = _ISSUE_RE.match(block)
        if not match:
            report.other_blocks.append(block)
            continue
        who = _SAY_WHO_RE.search(block)
        if who:
            report.say_who_counts[who.group(1)] += 1
            continue
        report.issues.append(
            LintIssue(file=match.group(1), line=int(match.group(2)), text=block[match.end():].strip())
        )
    return report


def read_sdk_path(project_root: Path, fallback: Path) -> Path:
    """Read the SDK location from .renpy-sdk, which the VS Code extension writes as UTF-16."""
    marker = project_root / ".renpy-sdk"
    if marker.exists():
        raw = marker.read_bytes()
        encoding = "utf-16" if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else (
            "utf-16-le" if len(raw) > 1 and raw[1] == 0 else "utf-8"
        )
        value = raw.decode(encoding, errors="replace").strip().strip("﻿")
        if value:
            return Path(value)
    return fallback


@dataclass(frozen=True, slots=True)
class LintRun:
    report: LintReport | None
    parse_errors: str | None
    duration_seconds: float
    stdout: str


def run_lint(project_root: Path, sdk_path: Path, timeout_seconds: float) -> LintRun:
    """Run Ren'Py lint without clobbering the runtime log.

    Lint rewrites log.txt, so it is backed up and restored. Parse errors never
    reach the lint report: Ren'Py writes them to errors.txt instead, which we
    detect by its mtime moving past the start of this run.
    """
    python = sdk_path / "lib" / "py3-windows-x86_64" / "python.exe"
    renpy_py = sdk_path / "renpy.py"
    if not python.exists() or not renpy_py.exists():
        raise FileNotFoundError(
            f"Ren'Py SDK nicht gefunden unter {sdk_path} (erwartet {python} und {renpy_py}). "
            "Pfad in .renpy-sdk oder MTS_RENPY_SDK_PATH pruefen."
        )

    log_path = project_root / "log.txt"
    errors_path = project_root / "errors.txt"

    with tempfile.TemporaryDirectory(prefix="mts-lint-") as tmp:
        tmp_dir = Path(tmp)
        log_backup = tmp_dir / "log.txt.bak"
        report_path = tmp_dir / "lint.txt"
        if log_path.exists():
            shutil.copy2(log_path, log_backup)

        env = dict(os.environ, SDL_AUDIODRIVER="dummy")
        started = time.time()
        try:
            completed = subprocess.run(
                [str(python), str(renpy_py), str(project_root), "lint", str(report_path)],
                # The MCP server's own stdin is the JSON-RPC pipe. Inherited, it hangs
                # Ren'Py's interpreter at startup (0 CPU, until the timeout).
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                timeout=timeout_seconds,
                cwd=str(project_root),
            )
        finally:
            if log_backup.exists():
                shutil.copy2(log_backup, log_path)
        duration = time.time() - started

        parse_errors = None
        # 1s slack: errors.txt mtime can land a hair before our wall-clock start on NTFS.
        if errors_path.exists() and errors_path.stat().st_mtime >= started - 1:
            parse_errors = errors_path.read_text(encoding="utf-8-sig", errors="replace")

        report = None
        if report_path.exists():
            report = parse_lint_report(report_path.read_text(encoding="utf-8-sig", errors="replace"))

    return LintRun(
        report=report,
        parse_errors=parse_errors,
        duration_seconds=duration,
        stdout=(completed.stdout or "") + (completed.stderr or ""),
    )


def format_lint_run(
    run: LintRun,
    *,
    path_filter: str | None = None,
    show_say_names: bool = False,
    max_issues: int = 200,
) -> str:
    """Render a lint run as a compact text answer for the MCP client."""
    lines = [f"# Ren'Py lint ({run.duration_seconds:.1f}s)"]

    if run.parse_errors is not None:
        lines += [
            "",
            "## PARSE-FEHLER (errors.txt) — Lint-Report wurde nicht erzeugt",
            run.parse_errors.strip(),
        ]
        return "\n".join(lines)

    if run.report is None:
        lines += ["", "Kein Lint-Report erzeugt. Ausgabe von Ren'Py:", run.stdout.strip() or "(leer)"]
        return "\n".join(lines)

    needle = path_filter.replace("\\", "/").lower() if path_filter else None
    issues = [
        issue for issue in run.report.issues
        if needle is None or needle in issue.file.lower() or needle in issue.text.lower()
    ]

    scope = f" (Filter: '{path_filter}')" if path_filter else ""
    lines += ["", f"## {len(issues)} echte Befunde{scope}"]
    for issue in issues[:max_issues]:
        lines.append(f"- {issue.file}:{issue.line} {issue.text}")
    if len(issues) > max_issues:
        lines.append(f"... {len(issues) - max_issues} weitere abgeschnitten (max_issues erhoehen)")
    if not issues:
        lines.append("(keine)")

    for block in run.report.other_blocks:
        lines += ["", block]

    say_total = sum(run.report.say_who_counts.values())
    lines += [
        "",
        f"## Say-who-Rauschen: {say_total} Zeilen, {len(run.report.say_who_counts)} Namen ausgeblendet",
        "(Person-Charaktere entstehen erst zur Laufzeit; seltene Namen koennen Tippfehler sein.)",
    ]
    if show_say_names:
        # Rarest first: a misspelled speaker shows up once or twice, real ones dozens of times.
        for name, count in sorted(run.report.say_who_counts.items(), key=lambda item: (item[1], item[0])):
            lines.append(f"- {name}: {count}")

    return "\n".join(lines)
