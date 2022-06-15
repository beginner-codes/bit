import sqlalchemy.ext.asyncio
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bit.config import load_config


def connect(settings=Depends(load_config)):
    return sqlalchemy.ext.asyncio.create_async_engine(settings.db_uri)


def session_maker(database=Depends(connect)):
    return sessionmaker(database, expire_on_commit=False, class_=AsyncSession)
