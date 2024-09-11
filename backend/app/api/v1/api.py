from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_restful.cbv import cbv

from app.crud import crud_api, crud_api_group
from app.schemas.api import (
    ApiGroupCreate,
    ApiGroupDetailRead,
    ApiGroupRead,
    ApiGroupUpdate,
    ApiRead,
    ApiUpdate,
)
from app.utils.enums import APIAccess

router = APIRouter()


@cbv(router)
class ApiGroupView:
    @router.get(
        '/api-groups',
        name=APIAccess.PRIVATE,
        summary='全部 Api 群組資料',
        status_code=status.HTTP_200_OK,
        tags=['Api 群組'],
    )
    async def get_multi(self) -> list[ApiGroupDetailRead]:
        items = await crud_api_group.get_multi()
        return items

    @router.post(
        '/api-groups',
        name=APIAccess.PRIVATE,
        summary='新增 Api 群組資料',
        status_code=status.HTTP_201_CREATED,
        tags=['Api 群組'],
    )
    async def create(self, item: ApiGroupCreate) -> ApiGroupRead:
        instance = await crud_api_group.create(create_item=item)
        return instance

    @router.get(
        '/api-groups/{api_group_id}',
        name=APIAccess.PRIVATE,
        summary='取得 Api 群組資料',
        status_code=status.HTTP_200_OK,
        tags=['Api 群組'],
    )
    async def get(self, api_group_id: UUID) -> ApiGroupRead:
        instance = await crud_api_group.get(item_id=api_group_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    @router.patch(
        '/api-groups/{api_group_id}',
        name=APIAccess.PRIVATE,
        summary='更新 Api 群組資料',
        status_code=status.HTTP_200_OK,
        tags=['Api 群組'],
    )
    async def update(
        self,
        api_group_id: UUID,
        item: ApiGroupUpdate,
    ) -> ApiGroupRead:
        instance = await crud_api_group.get(item_id=api_group_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_api_group.update(
            current_item=instance,
            update_item=item,
        )
        return instance

    @router.patch(
        '/api-groups/{api_group_id}/api-ids',
        name=APIAccess.PRIVATE,
        summary='更新 Api 群組資料',
        status_code=status.HTTP_200_OK,
        tags=['Api 群組'],
    )
    async def update_api_ids(
        self,
        api_group_id: UUID,
        api_ids: set[UUID],
    ) -> ApiGroupDetailRead:
        instance = await crud_api_group.get(item_id=api_group_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if not api_ids:
            return instance
        api_items = await crud_api.get_by_ids(list_ids=api_ids)
        instance = await crud_api_group.update_api_ids(
            current_item=instance,
            api_items=api_items,
        )
        return instance

    @router.delete(
        '/api-groups/{api_group_id}',
        name=APIAccess.PRIVATE,
        summary='刪除 Api 群組資料',
        status_code=status.HTTP_204_NO_CONTENT,
        tags=['Api 群組'],
    )
    async def destroy(self, api_group_id: UUID):
        await crud_api_group.destroy(item_id=api_group_id)


@cbv(router)
class ApiView:
    @router.get(
        '/apis',
        name=APIAccess.PRIVATE,
        summary='全部 Api 資料',
        status_code=status.HTTP_200_OK,
        tags=['Api'],
    )
    async def get_multi(self) -> list[ApiRead]:
        items = await crud_api.get_multi()
        return items

    @router.patch(
        '/apis/{api_id}',
        name=APIAccess.PRIVATE,
        summary='更新 Api 資料',
        status_code=status.HTTP_200_OK,
        tags=['Api'],
    )
    async def update(
        self,
        api_id: UUID,
        item: ApiUpdate,
    ) -> ApiRead:
        instance = await crud_api.get(item_id=api_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_api.update(
            current_item=instance,
            update_item=item,
        )
        return instance
