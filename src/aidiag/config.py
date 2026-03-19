"""Configurações centrais da aplicação."""

from __future__ import annotations

import secrets
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configurações carregadas via variáveis de ambiente ou .env."""

    app_name: str = "AI Industry Diagnostics"
    database_url: str = f"sqlite:///{BASE_DIR / 'aidiag.db'}"
    secret_key: str = secrets.token_urlsafe(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    upload_dir: str = str(BASE_DIR / "uploads")
    api_port: int = 8000
    dashboard_port: int = 8501

    model_config = {"env_prefix": "AIDIAG_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
