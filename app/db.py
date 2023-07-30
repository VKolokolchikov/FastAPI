"""Db session"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings


engine = create_async_engine(settings.db_url, echo=settings.db_logs, pool_pre_ping=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

if settings.db_url_ro is None or settings.db_url == settings.db_url_ro:
    engine_ro = engine
    async_session_ro = async_session
else:
    engine_ro = create_async_engine(settings.db_url_ro, echo=settings.db_logs, pool_pre_ping=True)
    async_session_ro = sessionmaker(
        engine_ro, class_=AsyncSession, expire_on_commit=False
    )


def get_session(read_only: bool = False) -> AsyncSession:
    """Return db session"""
    if read_only:
        return async_session_ro()

    return async_session()
