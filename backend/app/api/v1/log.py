from uuid import UUID
from fastapi import status, HTTPException, APIRouter
from fastapi_pagination import add_pagination
from fastapi_restful.cbv import cbv

from app.crud import crud_user_log, crud_system_log
from app.dependencies.base import web_params
from app.dependencies.query.log import SuperUserLogQuery
from app.dependencies.query.system import SystemLogQuery
from app.schemas.log import UserLogRead, SystemLogRead, AllUserLogRead
from app.utils.enums import APIAccess
from app.utils.pagination import Page
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
    ) -> Page[AllUserLogRead]:
        items = await crud_user_log.get_multi(query=query, paginated=True)
        return items

    @router.get(
        '/log/systems',
        name=APIAccess.PRIVATE,
        summary='系統日誌列表',
        status_code=status.HTTP_200_OK,
        tags=['日誌'],
    )
    async def get_multi_systems(
        self,
        query: QueryList = web_params(SystemLogQuery),
    ) -> list[SystemLogRead]:
        items = await crud_user_log.get_multi(query=query)
        return items

    @router.get(
        '/log/systems/{log_id}',
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


add_pagination(router)
