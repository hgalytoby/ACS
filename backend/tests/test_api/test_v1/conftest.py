from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient
import pytest


@pytest.fixture
async def test_client(
    get_app: FastAPI,
    get_superuser_bearer_token_header: dict[str, str],
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=get_app,
        base_url='http://app.io/api/v1',
        headers=get_superuser_bearer_token_header,
    ) as test_client:
        yield test_client
