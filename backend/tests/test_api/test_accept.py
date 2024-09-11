from fastapi import status
from httpx import AsyncClient
import pytest

from app.utils.enums import SteinsGate


@pytest.fixture
def accept_test_client(
    test_client: AsyncClient,
    get_accept_header: dict[str, SteinsGate],
) -> AsyncClient:
    test_client.headers = get_accept_header
    return test_client


@pytest.mark.AcceptView
@pytest.mark.View
class TestAcceptLocationView:
    @pytest.mark.parametrize('url', ['/accept-location', '/accept-api'])
    async def test_dependencies_valid_accept_token_fail_empty(
        self,
        test_client: AsyncClient,
        url: str,
    ):
        res = await test_client.get(url=url)
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize('url', ['/accept-location', '/accept-api'])
    async def test_dependencies_valid_accept_token_fail_valid(
        self,
        test_client: AsyncClient,
        url: str,
    ):
        res = await test_client.get(
            url=url,
            headers={'divergence': ''},
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.usefixtures('member_location')
    async def test_get_location(
        self,
        accept_test_client: AsyncClient,
    ):
        res = await accept_test_client.get(url='/accept-location')
        assert res.status_code == status.HTTP_200_OK
        assert res.json()

    @pytest.mark.usefixtures('accept_api')
    async def test_get_api(
        self,
        accept_test_client: AsyncClient,
    ):
        res = await accept_test_client.get(url='/accept-api')
        assert res.status_code == status.HTTP_200_OK
        assert res.json()

    async def test_get_api_fail_not_exist(
        self,
        accept_test_client: AsyncClient,
    ):
        res = await accept_test_client.get(url='/accept-api')
        assert res.status_code == status.HTTP_404_NOT_FOUND
