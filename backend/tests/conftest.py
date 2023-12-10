import asyncio
import random
from typing import Callable, Any, AsyncGenerator
from unittest.mock import MagicMock
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlmodel import SQLModel

from app.api import router
from app.core.config import settings
from app.crud import crud_member_location, crud_accept_api
from app.db.session import engine
from app.models import MemberLocationModel, AcceptApiModel
from app.utils.enums import SteinsGate

AsyncMethodMocker = Callable[..., MagicMock]

app = FastAPI()
app.include_router(router, prefix='/api')
app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.pg.url,
    custom_engine=engine,
)


@pytest.fixture(name='event_loop', scope='session')
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://app.io/api',
        ) as test_client:
            yield test_client


@pytest.fixture
def async_method_mocker(mocker: MockerFixture) -> AsyncMethodMocker:
    def _async_method_mocker(
        obj: Any,
        method: str,
        return_value: Any = None,
    ) -> MagicMock:
        mock: MagicMock = mocker.MagicMock()

        future = asyncio.Future()
        future.set_result(return_value)
        mock.return_value = future
        mock.side_effect = None

        setattr(obj, method, mock)

        return mock

    return _async_method_mocker


@pytest.fixture(autouse=True)
async def setup() -> AsyncGenerator[AsyncClient, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='session')
def get_accept_header() -> dict[str, SteinsGate]:
    return {'divergence': SteinsGate.DIVERGENCE}


@pytest.fixture
async def member_location() -> MemberLocationModel:
    item = MemberLocationModel(name=str(random.random()), image='')
    async with db():
        instance = await crud_member_location.create(
            create_item=item,
            image=None,
        )
        return instance


@pytest.fixture
async def accept_api() -> AcceptApiModel:
    item = AcceptApiModel(api='')
    async with db():
        instance = await crud_accept_api.create(create_item=item)
        return instance
