from pathlib import Path
from pydantic import BaseSettings, Extra
from functools import cache
import json


PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_PATHS = (PROJECT_ROOT / "settings.json", PROJECT_ROOT / "settings.dev.json")


class Settings(BaseSettings):
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    DEV: bool = False

    class Config:
        extra = Extra.allow
        env_prefix = "BIT_"


@cache
def load_config(*paths: Path) -> Settings:
    settings = load_settings(*paths or DEFAULT_PATHS)
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
