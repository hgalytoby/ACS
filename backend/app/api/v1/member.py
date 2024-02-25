from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi_pagination import add_pagination
from fastapi_restful.cbv import cbv

from app.core.config import settings
from app.crud import (
    crud_member,
    crud_member_location,
    crud_member_record,
    crud_member_status,
)
from app.dependencies.base import web_params
from app.dependencies.deps import authorize_api
from app.dependencies.query import MemberQuery, MemberRecordQuery
from app.schemas.member import (
    MemberCreate,
    MemberLocationCreate,
    MemberLocationRead,
    MemberLocationUpdate,
    MemberRead,
    MemberRecordRead,
    MemberStatusRead,
    MemberUpdate,
)
from app.schemas.websocket import WebSocketEventSchema
from app.utils.enums import APIAccess, WebSocketEvent
from app.utils.pagination import Page
from app.websocket import broadcast

router = APIRouter()


@cbv(router)
class MemberView:
    @router.get(
        '/members',
        name=APIAccess.PRIVATE,
        summary='全部成員資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get_multi(
        self,
        query=web_params(MemberQuery),
    ) -> Page[MemberRead]:
        items = await crud_member.get_multi(query=query, paginated=True)
        return items

    @router.post(
        '/members',
        name=APIAccess.PRIVATE,
        summary='新增成員資料',
        status_code=status.HTTP_201_CREATED,
        tags=['成員'],
    )
    async def create(
        self,
        item: MemberCreate,
        image: UploadFile = File(),
    ) -> MemberRead:
        instance = await crud_member.create(create_item=item, image=image)
        return instance

    @router.get(
        '/members/{member_id}',
        name=APIAccess.PRIVATE,
        summary='取得成員資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get(self, member_id: UUID) -> MemberRead:
        instance = await crud_member.get(item_id=member_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    @router.patch(
        '/members/{member_id}',
        name=APIAccess.PRIVATE,
        summary='更新成員資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def update(
        self,
        member_id: UUID,
        item: MemberUpdate,
        image: Optional[UploadFile] = File(None),
    ) -> MemberRead:
        instance = await crud_member.get(item_id=member_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_member.update(
            current_item=instance,
            update_item=item,
            image=image,
        )
        return instance

    @router.delete(
        '/members/{member_id}',
        name=APIAccess.PRIVATE,
        summary='刪除成員資料',
        status_code=status.HTTP_204_NO_CONTENT,
        tags=['成員'],
    )
    async def destroy(self, member_id: UUID):
        await crud_member.destroy(item_id=member_id)


@cbv(router)
class MemberRecordView:
    @router.get(
        '/members-record',
        name=APIAccess.PRIVATE,
        summary='全部成員紀錄資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
        dependencies=[Depends(authorize_api)],
    )
    async def get_multi(
        self,
        query=web_params(MemberRecordQuery),
    ) -> Page[MemberRecordRead]:
        items = await crud_member_record.get_multi(query=query, paginated=True)
        return items

    @router.get(
        '/members-record/{member_record_id}',
        name=APIAccess.PRIVATE,
        summary='取得成員紀錄資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get(self, member_record_id: UUID) -> MemberRecordRead:
        instance = await crud_member_record.get(item_id=member_record_id)
        return instance


@cbv(router)
class MemberLocationView:
    @classmethod
    async def publish_member_status_event(cls):
        message = WebSocketEventSchema(
            event=WebSocketEvent.MEMBER_STATUS_LIST,
        ).json()
        await broadcast.publish(channel=settings.project, message=message)

    @router.get(
        '/members-location',
        name=APIAccess.PRIVATE,
        summary='全部地點',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get_multi(self) -> list[MemberLocationRead]:
        items = await crud_member_location.get_multi()
        return items

    @router.post(
        '/members-location',
        name=APIAccess.PRIVATE,
        summary='新增地點',
        status_code=status.HTTP_201_CREATED,
        tags=['成員'],
    )
    async def create(
        self,
        item: MemberLocationCreate,
        image: UploadFile = File(),
    ) -> MemberLocationRead:
        instance = await crud_member_location.create(
            create_item=item,
            image=image,
        )
        await self.publish_member_status_event()
        return instance

    @router.get(
        '/members-location/{location_id}',
        name=APIAccess.PRIVATE,
        summary='取得地點資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get(self, location_id: UUID) -> MemberLocationRead:
        instance = await crud_member_location.get(item_id=location_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    @router.patch(
        '/members-location/{location_id}',
        name=APIAccess.PRIVATE,
        summary='更新地點資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def update(
        self,
        location_id: UUID,
        item: MemberLocationUpdate,
        image: Optional[UploadFile] = File(None),
    ) -> MemberLocationRead:
        instance = await crud_member_location.get(item_id=location_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_member_location.update(
            current_item=instance,
            update_item=item,
            image=image,
        )
        await self.publish_member_status_event()
        return instance

    @router.delete(
        '/members-location/{location_id}',
        name=APIAccess.PRIVATE,
        summary='刪除地點資料',
        status_code=status.HTTP_204_NO_CONTENT,
        tags=['成員'],
    )
    async def destroy(self, location_id: UUID):
        instance = await crud_member_location.get(item_id=location_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await crud_member_location.destroy(item_id=location_id)
        await self.publish_member_status_event()


@cbv(router)
class MemberStatusView:
    @router.get(
        '/members-status',
        name=APIAccess.PRIVATE,
        summary='取得全部進出資料',
        status_code=status.HTTP_200_OK,
        tags=['成員'],
    )
    async def get_multi(self) -> list[MemberStatusRead]:
        return await crud_member_status.get_multi()


add_pagination(router)
