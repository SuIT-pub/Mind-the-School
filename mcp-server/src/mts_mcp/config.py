from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the Mind the School MCP server."""

    model_config = SettingsConfigDict(env_prefix="MTS_", env_file=".env", extra="ignore")

    project_root: Path = Path.cwd().parent

    @property
    def log_path(self) -> Path:
        return self.project_root / "log.txt"

    @property
    def traceback_path(self) -> Path:
        return self.project_root / "traceback.txt"


@lru_cache
def settings() -> Settings:
    return Settings()
