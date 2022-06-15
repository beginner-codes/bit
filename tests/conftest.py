import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from bit.config import Settings
from bit.models import Base


class Fuzzy:
    def __init__(self, type):
        self.type = type

    def __eq__(self, other):
        return isinstance(other, self.type)

    def __repr__(self):
        return f"Any[{self.type.__name__}]"


@pytest.fixture
def config():
    return Settings()


@pytest.fixture()
async def database(config):
    db = create_async_engine(config.db_uri)
    async with db.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return db
