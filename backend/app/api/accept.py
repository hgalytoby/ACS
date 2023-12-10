from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from fastapi import status, APIRouter, Request, HTTPException
from redis.exceptions import LockError

from app.core.config import settings
from app.dependencies.deps import valid_accept_token
from app.crud import crud_member_location, crud_accept_api, crud_member_status
from app.schemas.accept import AcceptApiRead
from app.schemas.member import MemberLocationRead, MemberStatusCreate, MemberStatusCreatedRead
from app.schemas.websocket import WebSocketEventSchema
from app.utils.enums import APIAccess, WebSocketEvent
from app.websocket import broadcast

router = APIRouter()


@cbv(router)
class AcceptLocationView:
    @router.get(
        '/accept-location',
        name=APIAccess.PUBLIC,
        summary='全部地區資料',
        status_code=status.HTTP_200_OK,
        tags=['Accept'],
        dependencies=[Depends(valid_accept_token)],
    )
    async def get_location(self) -> list[MemberLocationRead]:
        items = await crud_member_location.get_multi()
        return items

    @router.get(
        '/accept-api',
        name=APIAccess.PUBLIC,
        summary='取得 QrCode Api',
        status_code=status.HTTP_200_OK,
        tags=['Accept'],
        dependencies=[Depends(valid_accept_token)],
    )
    async def get_api(self) -> AcceptApiRead:
        instance = await crud_accept_api.get_first()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return instance

    @router.post(
        '/accept-member-status',
        name=APIAccess.PUBLIC,
        summary='新增成員進出資料',
        status_code=status.HTTP_200_OK,
        tags=['Accept'],
    )
    async def create(
        self,
        item: MemberStatusCreate,
        request: Request,
    ) -> MemberStatusCreatedRead:
        redis = request.state.redis
        try:
            async with redis.lock(item.member_id.hex, blocking_timeout=0.1, timeout=0.5):
                result = await crud_member_status.create(create_item=item)
                message = WebSocketEventSchema(
                    event=WebSocketEvent.MEMBER_STATUS,
                    data=result,
                ).json()
                await broadcast.publish(channel=settings.project, message=message)
        except LockError:
            raise HTTPException(status_code=status.HTTP_423_LOCKED, detail='too fast.')
        else:
            message = WebSocketEventSchema(event=WebSocketEvent.MEMBER_STATUS_LIST).json()
            await broadcast.publish(channel=settings.project, message=message)
            return result
