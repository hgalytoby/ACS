import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Awaitable, Callable, Optional
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from fastapi_async_sqlalchemy import db
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient
from pytest_mock import MockerFixture
from redis.exceptions import LockError
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.crud import crud_user, crud_accept_api, crud_member_location
from app.db.session import engine, async_session_maker
from app.main import app
from app.models import (
    UserModel,
    UserBase,
    AcceptApiModel,
    AcceptApiBase,
    MemberLocationModel,
    MemberLocationBase,
)
from app.utils.enums import SteinsGate

AsyncMethodMocker = Callable[..., MagicMock]

password_helper = PasswordHelper()
pytest_password = password_helper.hash('string')


@pytest.fixture(name='event_loop', scope='session')
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def get_superuser(
    get_async_session: AsyncSession,
    create_user_payload: Callable[..., UserBase],
):
    item = create_user_payload(
        model=UserModel,
        is_superuser=True,
        is_verified=True,
        hashed_password=pytest_password,
    )
    instance = await crud_user.create(db_session=get_async_session, create_item=item)
    return instance


@pytest.fixture
async def get_app(get_superuser) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def test_client(get_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
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


class RedisMock:
    store: dict[str, tuple[str, Optional[int]]]

    def __init__(self):
        self.store = {}

    async def get(self, key: str) -> Optional[str]:
        try:
            value, expiration = self.store[key]
            if expiration is not None and expiration < datetime.now().timestamp():
                return None
            return value
        except KeyError:
            return None

    async def set(self, key: str, value: str, ex: Optional[int] = None):
        expiration = None
        if ex is not None:
            expiration = int(datetime.now().timestamp() + ex)
        self.store[key] = (value, expiration)

    async def delete(self, key: str):
        try:
            del self.store[key]
        except KeyError:
            pass

    async def close(self):
        pass

    @asynccontextmanager
    async def lock(self, key: str, blocking_timeout: float = 0.1, timeout: float = 0.5):
        start_time = datetime.now().timestamp()
        while True:
            value = await self.get(key)
            if value is None:
                await self.set(key, 'locked', ex=int(timeout))
                yield self
                await self.delete(key)
                return
            elif (
                blocking_timeout == 0
                or (datetime.now().timestamp() - start_time) > blocking_timeout
            ):
                raise LockError('Lock not acquired')
            await asyncio.sleep(0.1)


@pytest.fixture(scope='session', autouse=True)
def redis_mock() -> RedisMock:
    return RedisMock()


@pytest.fixture(autouse=True)
def set_redis_mock(
    redis_mock: RedisMock,
    mocker: MockerFixture,
):
    for obj in (
        'app.crud.user.init_redis_pool',
        'app.main.init_redis_pool',
    ):
        mock = mocker.patch(obj)
        mock.return_value = redis_mock


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
def create_headers_bearer_token(
    redis_mock: RedisMock,
) -> Callable[..., Awaitable[dict[str, str]]]:
    async def _(
        user: UserModel,
    ) -> dict[str, str]:
        key_prefix = settings.token_key_prefix
        token = uuid4().hex
        key = f'{key_prefix}{token}'
        await redis_mock.set(key, str(user.id))
        return {'Authorization': f'bearer {token}'}

    return _


@pytest.fixture
async def get_superuser_bearer_token_header(
    create_headers_bearer_token: Callable[..., Awaitable[dict[str, str]]],
    get_superuser: UserModel,
) -> dict[str, str]:
    return await create_headers_bearer_token(user=get_superuser)


@pytest.fixture
def create_member_location_payload() -> Callable[..., MemberLocationBase]:
    def func(
        model: type[MemberLocationBase],
        **kwargs: dict[Any, Any],
    ) -> MemberLocationBase:
        data = {'name': uuid4().hex} | kwargs
        payload = model(**data)
        return payload

    return func


@pytest.fixture
async def member_location(
    create_member_location_payload: Callable[..., MemberLocationModel],
) -> MemberLocationModel:
    item = create_member_location_payload(
        model=MemberLocationModel,
        image='',
    )
    async with db():
        instance = await crud_member_location.create(
            create_item=item,
            image=None,
        )
        return instance


@pytest.fixture
def create_accept_api_payload() -> Callable[..., AcceptApiBase]:
    def func(
        model: type[AcceptApiBase],
        **kwargs: dict[Any, Any]
    ) -> AcceptApiBase:
        data = {'api': '/api/test'} | kwargs
        payload = model(**data)
        return payload

    return func


@pytest.fixture
async def accept_api(
    create_accept_api_payload: Callable[..., AcceptApiModel],
) -> AcceptApiModel:
    item = create_accept_api_payload(model=AcceptApiModel)
    async with db():
        instance = await crud_accept_api.create(create_item=item)
        return instance


@pytest.fixture
def create_user_payload() -> Callable[..., UserBase]:
    def func(
        model: type[UserBase],
        **kwargs: dict[Any: Any],
    ) -> UserBase:
        default = {
            'email': 'pytest@gmail.com',
            'is_active': True,
            'is_superuser': False,
            'is_verified': False,
            'username': uuid4().hex,
        }
        data = default | kwargs
        payload = model(**data)
        return payload

    return func


@pytest.fixture
async def user(
    create_user_payload: Callable[..., UserModel],
) -> UserModel:
    item = create_user_payload(
        model=UserModel,
        hashed_password=pytest_password,
    )
    async with db():
        instance = await crud_user.create(item=item)
        return instance
