import sqlalchemy.ext.asyncio


def connect(settings):
    return sqlalchemy.ext.asyncio.create_async_engine(settings.uri)
