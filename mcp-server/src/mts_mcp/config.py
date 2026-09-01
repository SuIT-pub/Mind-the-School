from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the Mind the School MCP server.

    Environment variables use the ``MTS_`` prefix, e.g. ``MTS_OLLAMA_BASE_URL``.
    """

    model_config = SettingsConfigDict(env_prefix="MTS_", env_file=".env", extra="ignore")

    project_root: Path = Path.cwd().parent

    ollama_base_url: str = Field(
        default="http://127.0.0.1:11434",
        description="Ollama HTTP API base URL, e.g. http://192.168.1.10:11434.",
    )
    ollama_model: str = Field(
        default="",
        description="Default Ollama model name when a tool call omits `model`.",
    )
    ollama_timeout_seconds: float = Field(
        default=1800.0,
        ge=5.0,
        description="HTTP read timeout in seconds for Ollama generate/chat calls.",
    )
    ollama_num_ctx: int = Field(
        default=32768,
        ge=512,
        description="Ollama context window (num_ctx) for chat calls.",
    )
    ollama_max_tokens: int = Field(
        default=32768,
        ge=-1,
        description="Default generation cap (num_predict). -1 means no cap.",
    )

    @property
    def log_path(self) -> Path:
        return self.project_root / "log.txt"

    @property
    def traceback_path(self) -> Path:
        return self.project_root / "traceback.txt"

    @property
    def ollama_api_url(self) -> str:
        """Return the Ollama base URL without a trailing slash."""
        return self.ollama_base_url.strip().rstrip("/")


@lru_cache
def settings() -> Settings:
    return Settings()
