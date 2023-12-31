import pytest
from httpx import AsyncClient
from fastapi import status

from app.models import MemberLocationModel, AcceptApiModel
from app.utils.enums import SteinsGate


@pytest.mark.AcceptView
@pytest.mark.View
class TestAcceptLocationView:
    @pytest.mark.parametrize('url', ['/accept-location', '/accept-api'])
    async def test_dependencies_valid_accept_token_fail_empty(
        self,
        test_client: AsyncClient,
        url: str
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

    async def test_get_location(
        self,
        test_client: AsyncClient,
        get_accept_header: dict[str, SteinsGate],
        member_location: MemberLocationModel,
    ):
        res = await test_client.get(
            url='/accept-location',
            headers=get_accept_header,
        )
        assert res.status_code == status.HTTP_200_OK
        assert res.json()

    async def test_get_api(
        self,
        test_client: AsyncClient,
        get_accept_header: dict[str, SteinsGate],
        accept_api: AcceptApiModel,
    ):
        res = await test_client.get(
            url='/accept-api',
            headers=get_accept_header,
        )
        assert res.status_code == status.HTTP_200_OK

    async def test_get_api_fail_not_exist(
        self,
        test_client: AsyncClient,
        get_accept_header: dict[str, SteinsGate],
    ):
        res = await test_client.get(
            url='/accept-api',
            headers=get_accept_header,
        )
        assert res.status_code == status.HTTP_404_NOT_FOUND
