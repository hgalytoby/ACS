from typing import Awaitable, Callable

from httpx import AsyncClient
import pytest


@pytest.mark.ApiGroupView()
@pytest.mark.View()
class TestApiGroupView:
    async def test_get_multi(
        self,
        test_client: AsyncClient,
        get_superuser_bearer_token_header: dict[str, str],
    ):
        res = await test_client.get(
            url='/api-groups',
            headers=get_superuser_bearer_token_header,
        )
