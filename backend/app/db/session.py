from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel as BasePanel
from fastapi import Request

engine = create_async_engine(
    settings.pg.url,
    echo=False,
    pool_pre_ping=True,
    pool_size=8,
    max_overflow=64,
)
async_session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class SQLAlchemyPanel(BasePanel):
    async def add_engines(self, request: Request):
        self.engines.add(engine.sync_engine)
