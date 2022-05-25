from pathlib import Path
from pydantic import BaseSettings, Extra
from functools import cache
import json


class Settings(BaseSettings):
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        extra = Extra.allow
        env_prefix = "BIT_"


@cache
def open_config(path: Path) -> Settings:
    print("Loading file")
    with path.open("r") as file:
        return Settings(**json.load(file))
