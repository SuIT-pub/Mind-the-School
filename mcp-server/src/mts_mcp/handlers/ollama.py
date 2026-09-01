from __future__ import annotations

import os
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from mts_mcp.config import Settings
from mts_mcp.ollama_client import chat, fetch_ps, fetch_tags, fetch_version


def _ns(value: float | int | None) -> str:
    """Format an Ollama nanosecond duration as seconds.

    Args:
        value: Duration in nanoseconds, or None.

    Returns:
        A short seconds string, or ``-`` if missing.
    """
    if not isinstance(value, (int, float)) or value <= 0:
        return "-"
    return f"{value / 1_000_000_000:.1f}s"


def _bytes_label(size: int | None) -> str:
    """Format a byte size for model listings.

    Args:
        size: Size in bytes, or None.

    Returns:
        A human-readable size such as ``4.7 GB``.
    """
    if not isinstance(size, int) or size <= 0:
        return "-"
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(size)
    unit_index = 0
    while value >= 1024 and unit_index < len(units) - 1:
        value /= 1024
        unit_index += 1
    precision = 0 if unit_index < 2 else 1
    return f"{value:.{precision}f} {units[unit_index]}"


def _resolve_model(settings: Settings, model: str | None) -> str | None:
    """Pick the model name from the tool argument or the default setting.

    Args:
        settings: MCP runtime settings.
        model: Model name from the tool call, if any.

    Returns:
        A non-empty model name, or None if neither source provides one.
    """
    chosen = (model or "").strip() or settings.ollama_model.strip()
    return chosen or None


def _format_model_rows(models: list[Any]) -> str:
    """Render installed or loaded Ollama models as a plain-text list.

    Args:
        models: List of model dicts from ``/api/tags`` or ``/api/ps``.

    Returns:
        A newline-separated listing, or a placeholder if empty.
    """
    if not models:
        return "(keine)"
    lines: list[str] = []
    for item in models:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("model") or "?")
        details = item.get("details") if isinstance(item.get("details"), dict) else {}
        params = str(details.get("parameter_size") or "").strip()
        family = str(details.get("family") or "").strip()
        extras = [part for part in (params, family, _bytes_label(item.get("size"))) if part and part != "-"]
        suffix = f" ({', '.join(extras)})" if extras else ""
        lines.append(f"- {name}{suffix}")
    return "\n".join(lines) if lines else "(keine)"


def register(mcp: FastMCP, settings: Settings) -> None:
    """Expose the local Ollama instance as MCP tools for Cursor agents."""

    @mcp.tool(
        name="ollama_status",
        description=(
            "Prueft die Verbindung zur Ollama-Instanz auf dem Heimserver: "
            "API-URL, Version, Default-Modell und aktuell geladene Modelle."
        ),
    )
    async def ollama_status() -> str:
        """Return connectivity, version, default model, and loaded models."""
        version_result = await fetch_version(settings)
        if not version_result.ok:
            return version_result.error

        version = "-"
        if version_result.data:
            version = str(version_result.data.get("version") or "-")

        ps_result = await fetch_ps(settings)
        loaded = "(ps nicht verfuegbar)"
        if ps_result.ok and ps_result.data is not None:
            loaded = _format_model_rows(list(ps_result.data.get("models") or []))
        elif not ps_result.ok:
            loaded = ps_result.error

        default_model = settings.ollama_model.strip() or "(nicht gesetzt — model-Parameter an ollama_prompt uebergeben)"
        return "\n".join(
            [
                f"pid: {os.getpid()}",
                f"code: {__file__}",
                f"url: {settings.ollama_api_url}",
                f"version: {version}",
                f"default_model: {default_model}",
                f"num_ctx: {settings.ollama_num_ctx}",
                f"max_tokens: {settings.ollama_max_tokens}",
                f"timeout_s: {settings.ollama_timeout_seconds:.0f}",
                "loaded_models:",
                loaded,
            ]
        )

    @mcp.tool(
        name="ollama_list_models",
        description=(
            "Listet die auf der Ollama-Instanz installierten Modelle. "
            "Nutze den Namen (inkl. Tag) als `model` bei ollama_prompt."
        ),
    )
    async def ollama_list_models() -> str:
        """Return installed Ollama models from /api/tags."""
        result = await fetch_tags(settings)
        if not result.ok:
            return result.error
        models = list((result.data or {}).get("models") or [])
        listing = _format_model_rows(models)
        return f"Ollama {settings.ollama_api_url}\n{listing}"

    @mcp.tool(
        name="ollama_prompt",
        description=(
            "Schickt einen Prompt an ein Ollama-Modell auf dem Heimserver und "
            "gibt die Modellantwort zurueck. Nutze das, wenn eine lokale "
            "Modell-Meinung, ein Draft oder eine zweite Perspektive in die "
            "eigene Arbeit einfliessen soll. `model` ist der Ollama-Name "
            "(siehe ollama_list_models); ohne Angabe gilt MTS_OLLAMA_MODEL."
        ),
    )
    async def ollama_prompt(
        prompt: Annotated[
            str,
            Field(description="Der Prompt, der an das Modell gesendet wird."),
        ],
        model: Annotated[
            str | None,
            Field(
                description=(
                    "Ollama-Modellname inkl. Tag, z.B. llama3.2:latest. "
                    "Leer = Default aus MTS_OLLAMA_MODEL."
                )
            ),
        ] = None,
        system: Annotated[
            str | None,
            Field(description="Optionale System-Nachricht (Rolle, Constraints, Stil)."),
        ] = None,
        temperature: Annotated[
            float | None,
            Field(description="Optionale Sampling-Temperature (0.0–2.0)."),
        ] = None,
        max_tokens: Annotated[
            int | None,
            Field(
                description=(
                    "Limit fuer generierte Tokens (Ollama num_predict). "
                    "Default 32768; -1 = kein Limit."
                )
            ),
        ] = None,
        num_ctx: Annotated[
            int | None,
            Field(
                description=(
                    "Kontextfenster in Tokens (Ollama num_ctx). Default 32768."
                )
            ),
        ] = None,
        timeout_seconds: Annotated[
            float | None,
            Field(description="Optionales Read-Timeout in Sekunden fuer diesen Aufruf."),
        ] = None,
        think: Annotated[
            bool | None,
            Field(description="Falls gesetzt: Thinking des Modells an- oder ausschalten."),
        ] = None,
    ) -> str:
        """Send a prompt to Ollama and return the assistant text plus metadata.

        Args:
            prompt: User prompt for the model.
            model: Ollama model name; falls back to ``MTS_OLLAMA_MODEL``.
            system: Optional system message.
            temperature: Optional sampling temperature.
            max_tokens: Optional generation cap (``num_predict``); default 32768.
            num_ctx: Optional context window; default 32768.
            timeout_seconds: Optional per-call read timeout.
            think: Optional Ollama thinking flag.

        Returns:
            The model reply, or a German error string if the call failed.
        """
        text = prompt.strip() if prompt else ""
        if not text:
            return "Fehler: `prompt` ist leer."

        chosen_model = _resolve_model(settings, model)
        if not chosen_model:
            return (
                "Fehler: kein Modell angegeben. Uebergib `model` oder setze "
                "MTS_OLLAMA_MODEL in .cursor/mcp.json. "
                "Verfuegbare Modelle: Tool ollama_list_models."
            )

        result = await chat(
            settings,
            model=chosen_model,
            prompt=text,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            num_ctx=num_ctx,
            timeout_seconds=timeout_seconds,
            think=think,
        )
        if not result.ok:
            extra = ""
            if result.status_code == 404:
                extra = " Pruefe den Modellnamen mit ollama_list_models."
            return result.error + extra

        data = result.data or {}
        message = data.get("message") if isinstance(data.get("message"), dict) else {}
        content = str(message.get("content") or "").strip()
        thinking = str(message.get("thinking") or "").strip()
        if not content and not thinking:
            return (
                f"Ollama ({chosen_model}) lieferte eine leere Antwort. "
                f"done_reason={data.get('done_reason') or '-'}"
            )

        header = [
            f"model: {data.get('model') or chosen_model}",
            f"done_reason: {data.get('done_reason') or '-'}",
            f"duration: {_ns(data.get('total_duration'))}",
            f"eval_count: {data.get('eval_count') if data.get('eval_count') is not None else '-'}",
            f"prompt_eval_count: {data.get('prompt_eval_count') if data.get('prompt_eval_count') is not None else '-'}",
        ]
        sections = ["---", *header, "---", ""]
        if thinking:
            sections.extend(["[thinking]", thinking, "[/thinking]", ""])
        if content:
            sections.append(content)
        return "\n".join(sections).rstrip() + "\n"
