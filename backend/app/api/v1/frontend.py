from uuid import UUID
from fastapi_restful.cbv import cbv
from fastapi import status, HTTPException, APIRouter

from app.crud import crud_frontend
from app.models import FrontendModel
from app.schemas.frontend import FrontendRead, FrontendCreate, FrontendUpdate
from app.utils.enums import APIAccess

router = APIRouter()


@cbv(router)
class FrontendView:
    @router.get(
        '/frontend',
        name=APIAccess.PRIVATE,
        summary='全部前端資料',
        status_code=status.HTTP_200_OK,
        tags=['前端'],
    )
    async def get_multi(self) -> list[FrontendRead]:
        items = await crud_frontend.get_multi()
        return items

    @router.post(
        '/frontend',
        name=APIAccess.PRIVATE,
        summary='新增前端資料',
        status_code=status.HTTP_201_CREATED,
        tags=['前端']
    )
    async def create(self, item: FrontendCreate) -> FrontendRead:
        if item.parent_id:
            parent = await crud_frontend.get(item_id=item.parent_id)
            if not parent:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            item = FrontendModel(depth=parent.depth + 1, **item.dict())
        instance = await crud_frontend.create(create_item=item)
        return instance

    @router.get(
        '/frontend/{frontend_id}',
        name=APIAccess.PRIVATE,
        summary='取得前端資料',
        status_code=status.HTTP_200_OK,
        tags=['前端']
    )
    async def get(self, frontend_id: UUID) -> FrontendRead:
        instance = await crud_frontend.get(item_id=frontend_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    @router.patch(
        '/frontend/{frontend_id}',
        name=APIAccess.PRIVATE,
        summary='更新前端資料',
        status_code=status.HTTP_200_OK,
        tags=['前端']
    )
    async def update(
        self,
        frontend_id: UUID,
        item: FrontendUpdate,
    ) -> FrontendRead:
        instance = await crud_frontend.get(item_id=frontend_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_frontend.update(
            current_item=instance,
            update_item=item,
        )
        return instance

    @router.delete(
        '/frontend/{frontend_id}',
        name=APIAccess.PRIVATE,
        summary='刪除前端資料',
        status_code=status.HTTP_204_NO_CONTENT,
        tags=['前端'],
    )
    async def destroy(self, frontend_id: UUID):
        await crud_frontend.destroy(item_id=frontend_id)
