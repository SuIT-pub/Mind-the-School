from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from mts_mcp.config import Settings
from mts_mcp.lint import format_lint_run, read_sdk_path, run_lint

_DEFAULT_SDK = Path("M:/RenPy")


def register(mcp: FastMCP, settings: Settings) -> None:
    """Expose Ren'Py lint as a tool that filters out the Person say-who noise."""

    @mcp.tool(
        name="renpy_lint",
        description=(
            "Fuehrt Ren'Py lint fuer das Projekt aus (~20s) und liefert nur echte Befunde. "
            "Die ~1700 'Could not evaluate ... who part of a say statement'-Zeilen der "
            "Person-Charaktere werden zu einer Zaehlung zusammengefasst. Parse-Fehler "
            "(errors.txt) werden erkannt und statt des Reports geliefert. log.txt bleibt "
            "erhalten. `path_filter` grenzt auf Dateipfad/Text ein (z.B. 'new_management'); "
            "`show_say_names` listet die ausgeblendeten Sprecher, seltenste zuerst."
        ),
    )
    async def renpy_lint(
        path_filter: str | None = None,
        show_say_names: bool = False,
        max_issues: int = 200,
    ) -> str:
        sdk_path = settings.renpy_sdk_path or read_sdk_path(settings.project_root, _DEFAULT_SDK)
        try:
            # Lint blocks for ~20s; keep the stdio loop responsive meanwhile.
            run = await asyncio.to_thread(
                run_lint, settings.project_root, sdk_path, settings.lint_timeout_seconds
            )
        except FileNotFoundError as error:
            return f"# Ren'Py lint\n\n{error}"
        except subprocess.TimeoutExpired:
            return (
                f"# Ren'Py lint\n\nAbgebrochen nach {settings.lint_timeout_seconds:.0f}s "
                "(MTS_LINT_TIMEOUT_SECONDS). log.txt wurde wiederhergestellt."
            )
        return format_lint_run(
            run,
            path_filter=path_filter,
            show_say_names=show_say_names,
            max_issues=max(1, max_issues),
        )
