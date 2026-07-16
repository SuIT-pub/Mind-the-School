from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileReadResult:
    """Result of reading a project file for MCP tools and resources."""

    path: Path
    content: str
    exists: bool
    size_bytes: int
    modified_at: datetime | None


def read_project_file(path: Path, *, tail_lines: int | None = None) -> FileReadResult:
    """Read a text file from the project, optionally returning only the last N lines."""
    if not path.exists():
        return FileReadResult(
            path=path,
            content=f"Datei existiert noch nicht: {path.name}",
            exists=False,
            size_bytes=0,
            modified_at=None,
        )

    stat = path.stat()
    modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
    text = path.read_text(encoding="utf-8", errors="replace")

    if tail_lines is not None and tail_lines > 0:
        lines = text.splitlines()
        if len(lines) > tail_lines:
            text = "\n".join(lines[-tail_lines:])

    return FileReadResult(
        path=path,
        content=text,
        exists=True,
        size_bytes=stat.st_size,
        modified_at=modified_at,
    )


def format_file_header(result: FileReadResult) -> str:
    """Build a short metadata header for tool responses."""
    if not result.exists:
        return f"# {result.path.name}\n(status: nicht vorhanden)\n\n"

    modified = result.modified_at.isoformat() if result.modified_at else "unbekannt"
    return (
        f"# {result.path.name}\n"
        f"(groesse: {result.size_bytes} bytes, geaendert: {modified})\n\n"
    )
