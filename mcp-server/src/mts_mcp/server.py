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
            "Logs: Nutze get_renpy_logs / get_renpy_traceback nach Spielstart-Fehlern. "
            "Ollama: Bruecke zur lokalen Ollama-Instanz auf dem Heimserver. "
            "ollama_status prueft die Verbindung, ollama_list_models listet Modelle, "
            "ollama_prompt schickt einen Prompt an ein Modell. "
            "Nutze ollama_prompt, wenn eine lokale Modell-Antwort (Draft, zweite "
            "Perspektive, Laengen-Generierung) in die eigene Arbeit einfliessen soll — "
            "nicht als Ersatz fuer Projektwissen aus Wiki und Code. "
            "Uebergib `model`, wenn kein Default (MTS_OLLAMA_MODEL) gesetzt ist."
        ),
    )
    register_all_handlers(mcp, settings)
    return mcp


async def run(settings: Settings) -> None:
    _configure_logging()
    mcp = build_mcp(settings)
    await mcp.run_stdio_async()
