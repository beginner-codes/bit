from pathlib import Path
from pydantic import BaseSettings, Extra
from functools import cache
import json


class Settings(BaseSettings):
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    DEV: bool = False

    class Config:
        extra = Extra.allow
        env_prefix = "BIT_"


@cache
def open_config(*paths: Path) -> Settings:
    settings = {}
    for path in paths:
        try:
            with path.open("r") as file:
                settings |= json.load(file)
        except FileNotFoundError:
            pass

    return Settings(**settings)
