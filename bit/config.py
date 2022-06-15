import json
from functools import cache
from pathlib import Path

from pydantic import BaseSettings, Extra

PROJECT_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    DEV: bool = False
    db_uri: str = "sqlite+aiosqlite:///"

    class Config:
        extra = Extra.allow
        env_prefix = "BIT_"


@cache
def load_config() -> Settings:
    settings = load_settings(
        PROJECT_ROOT / "settings.json", PROJECT_ROOT / "settings.dev.json"
    )
    return Settings(**settings)


def load_settings(*paths: Path) -> dict:
    settings = {}
    for path in paths:
        try:
            with path.open("r") as file:
                settings |= json.load(file)
        except FileNotFoundError:
            pass

    return settings
