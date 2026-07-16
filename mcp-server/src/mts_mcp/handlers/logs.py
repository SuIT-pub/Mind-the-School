from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mts_mcp.config import Settings
from mts_mcp.files import format_file_header, read_project_file


def register(mcp: FastMCP, settings: Settings) -> None:
    """Expose Ren'Py log.txt and traceback.txt as MCP resources and tools."""

    @mcp.resource(
        "mts://logs/log.txt",
        name="Ren'Py log.txt",
        description="Ren'Py-Laufzeitlog des Projekts (log.txt im Projektroot).",
        mime_type="text/plain",
    )
    def renpy_log_resource() -> str:
        result = read_project_file(settings.log_path)
        return format_file_header(result) + result.content

    @mcp.resource(
        "mts://logs/traceback.txt",
        name="Ren'Py traceback.txt",
        description="Letzter Ren'Py-Fehlertraceback (traceback.txt im Projektroot).",
        mime_type="text/plain",
    )
    def renpy_traceback_resource() -> str:
        result = read_project_file(settings.traceback_path)
        return format_file_header(result) + result.content

    @mcp.tool(
        name="get_renpy_log",
        description=(
            "Liest log.txt aus dem Mind-the-School-Projektroot. "
            "Enthaelt Ren'Py-Startup, Performance und oft den vollstaendigen Traceback."
        ),
    )
    def get_renpy_log(tail_lines: int | None = None) -> str:
        """Return the contents of log.txt, optionally limited to the last N lines."""
        result = read_project_file(settings.log_path, tail_lines=tail_lines)
        return format_file_header(result) + result.content

    @mcp.tool(
        name="get_renpy_traceback",
        description=(
            "Liest traceback.txt aus dem Mind-the-School-Projektroot. "
            "Enthaelt den zuletzt aufgetretenen Ren'Py-Fehler."
        ),
    )
    def get_renpy_traceback(tail_lines: int | None = None) -> str:
        """Return the contents of traceback.txt, optionally limited to the last N lines."""
        result = read_project_file(settings.traceback_path, tail_lines=tail_lines)
        return format_file_header(result) + result.content

    @mcp.tool(
        name="get_renpy_logs",
        description=(
            "Liest log.txt und traceback.txt zusammen. "
            "Nuetzlich nach einem Spielstart-Fehler, um Kontext und Traceback auf einmal zu sehen."
        ),
    )
    def get_renpy_logs(tail_lines: int | None = None) -> str:
        """Return log.txt and traceback.txt in one response."""
        log_result = read_project_file(settings.log_path, tail_lines=tail_lines)
        traceback_result = read_project_file(settings.traceback_path, tail_lines=tail_lines)

        sections = [
            format_file_header(log_result).rstrip(),
            log_result.content,
            "",
            format_file_header(traceback_result).rstrip(),
            traceback_result.content,
        ]
        return "\n".join(sections)
