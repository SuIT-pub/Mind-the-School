from __future__ import annotations

from collections.abc import Callable

from mcp.server.fastmcp import FastMCP

from mts_mcp.config import Settings
from mts_mcp.handlers import logs

HandlerRegistrar = Callable[[FastMCP, Settings], None]

HANDLERS: tuple[HandlerRegistrar, ...] = (
    logs.register,
)


def register_all_handlers(mcp: FastMCP, settings: Settings) -> None:
    """Register every feature handler. Add new modules to HANDLERS to extend the server."""
    for register in HANDLERS:
        register(mcp, settings)
