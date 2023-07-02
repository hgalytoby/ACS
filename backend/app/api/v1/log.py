from uuid import UUID
from fastapi import status, HTTPException, APIRouter
from fastapi_restful.cbv import cbv

from app.crud import crud_user_log, crud_system_log
from app.dependencies.base import web_params
from app.dependencies.query.log import SuperUserLogQuery
from app.dependencies.query.system import SystemLogQuery
from app.schemas.log import UserLogRead, SystemLogRead
from app.utils.enums import APIAccess
from app.utils.sql_query import QueryList

router = APIRouter()


@cbv(router)
class LogView:
    @router.get(
        '/log/users',
        name=APIAccess.PRIVATE,
        summary='使用者日誌列表',
        status_code=status.HTTP_200_OK,
        tags=['日誌'],
    )
    async def get_multi_users(
            self,
            query: QueryList = web_params(SuperUserLogQuery),
    ) -> list[UserLogRead]:
        items = await crud_user_log.get_multi(query=query)
        return items

    @router.get(
        '/log/system',
        name=APIAccess.PRIVATE,
        summary='系統日誌列表',
        status_code=status.HTTP_200_OK,
        tags=['日誌'],
    )
    async def get_multi_system(
            self,
            query: QueryList = web_params(SystemLogQuery),
    ) -> list[SystemLogRead]:
        items = await crud_user_log.get_multi(query=query)
        return items

    @router.get(
        '/log/system/{log_id}',
        name=APIAccess.PRIVATE,
        summary='系統日誌',
        status_code=status.HTTP_200_OK,
        tags=['日誌'],
    )
    async def get_system(self, log_id: UUID) -> UserLogRead:
        instance = await crud_system_log.get(item_id=log_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserLogRead.from_orm(instance)
