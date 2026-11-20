"""Centralized server configuration for VIRALMIND AI."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv(env_path: Path) -> None:
    """Lightweight .env loader without external dependencies."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(BASE_DIR / ".env")


@dataclass
class Settings:
    env: str = field(default_factory=lambda: os.getenv("VIRALMIND_ENV", "development"))
    host: str = field(default_factory=lambda: os.getenv("VIRALMIND_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("VIRALMIND_PORT", "8000")))
    log_level: str = field(default_factory=lambda: os.getenv("VIRALMIND_LOG_LEVEL", "INFO"))
    db_path: Path = field(
        default_factory=lambda: BASE_DIR / os.getenv("VIRALMIND_DB_PATH", "database/viralmind.db")
    )
    api_token: str = field(default_factory=lambda: os.getenv("VIRALMIND_API_TOKEN", ""))
    default_provider: str = field(
        default_factory=lambda: os.getenv("VIRALMIND_DEFAULT_PROVIDER", "local").lower()
    )
    fallback_providers: List[str] = field(
        default_factory=lambda: [
            p.strip().lower()
            for p in os.getenv("VIRALMIND_FALLBACK_PROVIDERS", "local").split(",")
            if p.strip()
        ]
    )
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = field(
        default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
    )
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    enable_live_web: bool = field(
        default_factory=lambda: os.getenv("VIRALMIND_ENABLE_LIVE_WEB", "false").lower() == "true"
    )
    user_agent: str = field(
        default_factory=lambda: os.getenv(
            "VIRALMIND_USER_AGENT",
            "ViralMindAI/1.0 (+https://github.com/viralmind-ai/viralmind-ai)",
        )
    )


settings = Settings()
