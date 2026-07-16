from __future__ import annotations

import logging
import sys

from mcp.server.fastmcp import FastMCP

from mts_mcp.config import Settings
from mts_mcp.handlers import register_all_handlers


def _configure_logging(level: str = "WARNING") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.WARNING),
        stream=sys.stderr,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def build_mcp(settings: Settings) -> FastMCP:
    mcp = FastMCP(
        "mind-the-school",
        instructions=(
            "Mind the School (Ren'Py) Entwicklungsserver. "
            "Nutze die Log-Tools oder -Resources, um log.txt und traceback.txt "
            "nach Spielstart-Fehlern zu lesen."
        ),
    )
    register_all_handlers(mcp, settings)
    return mcp


async def run(settings: Settings) -> None:
    _configure_logging()
    mcp = build_mcp(settings)
    await mcp.run_stdio_async()
