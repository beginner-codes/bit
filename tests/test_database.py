from pytest import fixture, mark
import sqlalchemy.orm
import sqlalchemy.pool
import sqlalchemy.ext.asyncio

from bit.database import connect
from bit.models.base import Base
from bit.models.user import User


class DBSettings:
    uri = "sqlite+aiosqlite://"


@fixture
async def engine():
    engine = connect(DBSettings)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine


@mark.asyncio
async def test_database_migrations(engine):
    async with sqlalchemy.ext.asyncio.AsyncSession(engine) as session:
        session.add_all(
            [
                User(discord_id=1, name="Bob"),
                User(discord_id=2, name="Jill"),
                User(discord_id=3, name="Kyle"),
            ]
        )
        await session.commit()
        users = list(await session.scalars(sqlalchemy.select(User)))
        assert users[0].discord_id == 1
        assert users[1].discord_id == 2
        assert users[2].discord_id == 3
