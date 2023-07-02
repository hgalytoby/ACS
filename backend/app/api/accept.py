from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from fastapi import status, Request, APIRouter
from starlette.background import BackgroundTasks

from app.dependencies.deps import valid_accept_token
from app.crud import crud_member_location, crud_accept_api
from app.schemas.accept import AcceptApiRead
from app.schemas.member import MemberLocationRead
from app.utils.enums import APIAccess

router = APIRouter()


@cbv(router)
class AcceptLocationView:
    @router.get(
        '/accept-location',
        name=APIAccess.PUBLIC,
        summary='全部地區資料',
        status_code=status.HTTP_200_OK,
        tags=['accept'],
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
        tags=['accept'],
        dependencies=[Depends(valid_accept_token)],
    )
    async def get_api(self) -> AcceptApiRead:
        instance = await crud_accept_api.get_first()
        return instance
