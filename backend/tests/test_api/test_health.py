from fastapi import status
from httpx import AsyncClient
import pytest

from app.core.config import settings
from app.schemas.health import HealthRead


@pytest.mark.HealthView()
@pytest.mark.View()
class TestHealthView:
    async def test_health(self, test_client: AsyncClient):
        res = await test_client.get(url='/health')
        assert res.status_code == status.HTTP_200_OK

        health = HealthRead(**res.json())
        assert health.project == settings.project
