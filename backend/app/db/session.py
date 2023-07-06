from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from fastapi import Request

DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 10)

engine = create_async_engine(
    settings.pg.url,
    echo=False,
    pool_pre_ping=True,
    pool_size=POOL_SIZE,
    max_overflow=64,
    connect_args={
        'prepared_statement_cache_size': 0,
        'statement_cache_size': 0,
    }
)
async_session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class SQLAlchemyPanel(BasePanel):
    async def add_engines(self, request: Request):
        self.engines.add(engine.sync_engine)
