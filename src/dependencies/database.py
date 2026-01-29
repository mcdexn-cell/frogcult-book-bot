"""
Provide dependencies for database.
"""

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings

_engine = create_async_engine(url=settings.postgres_url, echo=False)
_session = async_sessionmaker(_engine)


def get_engine():
    return _engine


def get_session():
    return _session
