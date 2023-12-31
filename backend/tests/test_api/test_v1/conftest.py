from typing import AsyncGenerator
import pytest
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture
async def test_client(get_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=get_app,
        base_url='http://app.io/api/v1',
    ) as test_client:
        yield test_client
