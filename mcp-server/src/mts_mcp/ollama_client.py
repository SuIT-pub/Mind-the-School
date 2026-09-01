from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import httpx

from mts_mcp.config import Settings

_CONNECT_TIMEOUT_SECONDS = 10.0
_STATUS_TIMEOUT_SECONDS = 20.0
_USER_AGENT = "mts-mcp/0.1"


@dataclass(frozen=True, slots=True)
class OllamaHttpResult:
    """Outcome of a single HTTP call to the Ollama API."""

    ok: bool
    status_code: int
    data: dict[str, Any] | None
    error: str


def _timeout(read_seconds: float) -> httpx.Timeout:
    """Build an httpx timeout with a short connect limit and a long read limit.

    Args:
        read_seconds: Maximum seconds to wait for the response body.

    Returns:
        An ``httpx.Timeout`` instance.
    """
    return httpx.Timeout(
        connect=_CONNECT_TIMEOUT_SECONDS,
        read=read_seconds,
        write=30.0,
        pool=_CONNECT_TIMEOUT_SECONDS,
    )


def _headers() -> dict[str, str]:
    """Return default HTTP headers for Ollama requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": _USER_AGENT,
    }


def _connection_error(settings: Settings, exc: BaseException) -> str:
    """Format a connection failure so agents know how to fix the URL.

    Args:
        settings: Current MCP settings (used for the configured base URL).
        exc: The exception raised by httpx.

    Returns:
        A German error message including the configured URL.
    """
    return (
        f"Ollama ist nicht erreichbar unter {settings.ollama_api_url}. "
        f"Pruefe MTS_OLLAMA_BASE_URL in .cursor/mcp.json und ob der Dienst "
        f"auf dem Heimserver laeuft. Details: {exc}"
    )


async def ollama_request(
    settings: Settings,
    method: str,
    path: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout_seconds: float | None = None,
) -> OllamaHttpResult:
    """Call the Ollama HTTP API and return JSON or a structured error.

    Args:
        settings: MCP runtime settings (base URL, timeouts).
        method: HTTP method, e.g. ``GET`` or ``POST``.
        path: API path beginning with ``/``, e.g. ``/api/tags``.
        payload: Optional JSON body for POST requests.
        timeout_seconds: Optional read-timeout override in seconds.

    Returns:
        An ``OllamaHttpResult``. ``ok`` is True only for 2xx responses with JSON.
    """
    url = f"{settings.ollama_api_url}{path}"
    read_timeout = (
        timeout_seconds if timeout_seconds is not None else settings.ollama_timeout_seconds
    )

    try:
        async with httpx.AsyncClient(timeout=_timeout(read_timeout), headers=_headers()) as client:
            response = await client.request(method, url, json=payload)
    except httpx.TimeoutException:
        return OllamaHttpResult(
            ok=False,
            status_code=0,
            data=None,
            error=(
                f"Timeout nach {read_timeout:.0f}s bei {url}. "
                "Erhoehe MTS_OLLAMA_TIMEOUT_SECONDS oder timeout_seconds am Tool-Aufruf."
            ),
        )
    except httpx.RequestError as exc:
        return OllamaHttpResult(
            ok=False,
            status_code=0,
            data=None,
            error=_connection_error(settings, exc),
        )

    data: dict[str, Any] | None = None
    if response.content:
        try:
            parsed = response.json()
            if isinstance(parsed, dict):
                data = parsed
            else:
                data = {"data": parsed}
        except json.JSONDecodeError:
            text = response.text.strip() or "(leerer Body)"
            if response.is_success:
                return OllamaHttpResult(
                    ok=False,
                    status_code=response.status_code,
                    data=None,
                    error=f"Ollama lieferte kein JSON von {url}: {text[:500]}",
                )
            return OllamaHttpResult(
                ok=False,
                status_code=response.status_code,
                data=None,
                error=f"HTTP {response.status_code} von {url}: {text[:500]}",
            )

    if not response.is_success:
        api_error = ""
        if data:
            api_error = str(data.get("error") or data.get("message") or "")
        detail = api_error or (response.text.strip()[:500] if response.text else "kein Body")
        return OllamaHttpResult(
            ok=False,
            status_code=response.status_code,
            data=data,
            error=f"HTTP {response.status_code} von {url}: {detail}",
        )

    return OllamaHttpResult(
        ok=True,
        status_code=response.status_code,
        data=data or {},
        error="",
    )


async def fetch_version(settings: Settings) -> OllamaHttpResult:
    """GET /api/version.

    Args:
        settings: MCP runtime settings.

    Returns:
        HTTP result for the version endpoint.
    """
    return await ollama_request(
        settings, "GET", "/api/version", timeout_seconds=_STATUS_TIMEOUT_SECONDS
    )


async def fetch_tags(settings: Settings) -> OllamaHttpResult:
    """GET /api/tags (installed models).

    Args:
        settings: MCP runtime settings.

    Returns:
        HTTP result for the tags endpoint.
    """
    return await ollama_request(
        settings, "GET", "/api/tags", timeout_seconds=_STATUS_TIMEOUT_SECONDS
    )


async def fetch_ps(settings: Settings) -> OllamaHttpResult:
    """GET /api/ps (models currently loaded in memory).

    Args:
        settings: MCP runtime settings.

    Returns:
        HTTP result for the ps endpoint.
    """
    return await ollama_request(
        settings, "GET", "/api/ps", timeout_seconds=_STATUS_TIMEOUT_SECONDS
    )


async def chat(
    settings: Settings,
    *,
    model: str,
    prompt: str,
    system: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    num_ctx: int | None = None,
    timeout_seconds: float | None = None,
    think: bool | None = None,
) -> OllamaHttpResult:
    """POST /api/chat with a single user prompt (non-streaming).

    Args:
        settings: MCP runtime settings.
        model: Ollama model name, including tag (e.g. ``llama3.2:latest``).
        prompt: User message sent to the model.
        system: Optional system message.
        temperature: Optional sampling temperature.
        max_tokens: Optional ``num_predict`` cap. ``None`` uses the settings default.
        num_ctx: Optional context window. ``None`` uses the settings default.
        timeout_seconds: Optional read-timeout override.
        think: If set, request or disable model thinking (Ollama ``think`` flag).

    Returns:
        HTTP result for the chat endpoint.
    """
    messages: list[dict[str, str]] = []
    if system and system.strip():
        messages.append({"role": "system", "content": system.strip()})
    messages.append({"role": "user", "content": prompt})

    predict = settings.ollama_max_tokens if max_tokens is None else max_tokens
    context = settings.ollama_num_ctx if num_ctx is None else num_ctx

    options: dict[str, Any] = {
        "num_ctx": context,
        "num_predict": predict,
    }
    if temperature is not None:
        options["temperature"] = temperature

    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "keep_alive": "10m",
        "options": options,
    }
    if think is not None:
        payload["think"] = think

    return await ollama_request(
        settings,
        "POST",
        "/api/chat",
        payload=payload,
        timeout_seconds=timeout_seconds,
    )
