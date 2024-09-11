from typing import Awaitable, Callable
from uuid import UUID, uuid4

from fastapi import status
from httpx import AsyncClient
import pytest

from app import crud
from app.models import ApiGroupModel
from app.schemas.api import ApiGroupCreate, ApiGroupUpdate


@pytest.mark.ApiGroupView
@pytest.mark.View
class TestApiGroupView:
    @pytest.mark.usefixtures('api_group')
    async def test_get_multi(
        self,
        test_client: AsyncClient,
    ):
        res = await test_client.get(url='/api-groups')
        assert res.status_code
        assert res.json()

    async def test_get(
        self,
        test_client: AsyncClient,
        api_group: ApiGroupModel,
    ):
        res = await test_client.get(url=f'/api-groups/{api_group.id}')
        assert res.status_code == status.HTTP_200_OK
        assert UUID(res.json()['id']) == api_group.id

    @pytest.mark.parametrize(
        'method, model, status_code',
        [
            ('post', ApiGroupCreate, status.HTTP_201_CREATED),
            ('patch', ApiGroupUpdate, status.HTTP_200_OK),
        ],
    )
    async def test_create_or_update(
        self,
        test_client: AsyncClient,
        api_group: ApiGroupModel,
        create_api_group_payload: Callable[..., ApiGroupUpdate],
        assert_db_entry: Callable[..., Awaitable[None]],
        method: str,
        model: ApiGroupCreate | ApiGroupUpdate,
        status_code: int,
    ):
        payload = create_api_group_payload(
            model=model,
            name=uuid4().hex,
        )

        url, item_id = '/api-groups', None
        if method == 'patch':
            url += f'/{api_group.id}'
            item_id = api_group.id

        res = await getattr(test_client, method)(
            url=url,
            json=payload.dict(),
        )
        assert res.status_code == status_code

        await assert_db_entry(
            crud=crud.crud_api_group,
            item_id=item_id or res.json()['id'],
            payload=payload,
        )

    async def test_destroy(
        self,
        test_client: AsyncClient,
        api_group: ApiGroupModel,
        assert_db_entry_absence: Callable[..., Awaitable[None]],
    ):
        res = await test_client.delete(url=f'/api-groups/{api_group.id}')
        assert res.status_code == status.HTTP_204_NO_CONTENT

        await assert_db_entry_absence(
            crud=crud.crud_api_group,
            item_id=api_group.id,
        )
