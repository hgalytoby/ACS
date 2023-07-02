from uuid import UUID
from fastapi_restful.cbv import cbv
from fastapi import status, Depends, UploadFile, File, HTTPException, APIRouter

from app.crud import crud_role, crud_user_log
from app.dependencies.base import web_params
from app.dependencies.deps import authorize_api
from app.dependencies.query import UserExistQuery, UserQuery
from app.dependencies.query.log import UserLogQuery
from app.models import UserModel
from app.schemas.log import UserLogRead
from app.schemas.user import (
    UserRead,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserDetailRead,
)
from app.crud.user import (
    auth_backend,
    fastapi_users,
    crud_user,
    current_active_verified_user,
)
from app.utils.enums import UserFailDetail, APIAccess
from app.utils.sql_query import QueryList

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['授權'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['授權'],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['授權'],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['授權'],
)


@cbv(router)
class UserEmailExistView:
    @router.get(
        '/users/exist-email',
        name=APIAccess.PUBLIC,
        summary='檢查信箱使否存在',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
    )
    async def exist_email(self, query: QueryList = web_params(UserExistQuery)):
        if await crud_user.get_first(query=query):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserFailDetail.USER_EMAIL_EXIST,
            )


@cbv(router)
class UserView:
    user: UserModel = Depends(current_active_verified_user)

    @router.get(
        '/users',
        name=APIAccess.PRIVATE,
        summary='全部使用者',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
        dependencies=[Depends(authorize_api)],
    )
    async def get_multi_user(
            self,
            query: QueryList = web_params(UserQuery),
    ) -> list[UserRead]:
        users = await crud_user.get_multi(query=query)
        return users

    @router.patch(
        '/users/me/info',
        name=APIAccess.PRIVATE,
        summary='更新使用者 icon',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
    )
    async def update_info(
            self,
            item: UserUpdate,
            icon: UploadFile = File(None),
    ) -> UserRead:
        instance = await crud_user.update_info(
            user=self.user,
            update_item=item,
            icon=icon,
        )
        return instance

    @router.patch(
        '/users/me/update-password',
        name=APIAccess.PRIVATE,
        summary='修改密碼',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
    )
    async def update_password(
            self,
            item: UserPasswordUpdate,
    ) -> UserRead:
        instance = await crud_user.update_password(user=self.user, password=item)
        return instance

    @router.get(
        '/users/me/log',
        name=APIAccess.PRIVATE,
        summary='使用者日誌列表',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
    )
    async def get_multi_log(
            self,
            query: QueryList = web_params(UserLogQuery),
    ) -> list[UserLogRead]:
        items = await crud_user_log.get_multi(query=query)
        return items

    @router.get(
        '/users/me/log/{log_id]',
        name=APIAccess.PRIVATE,
        summary='使用者日誌',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
    )
    async def get(self, log_id: UUID) -> UserLogRead:
        instance = await crud_user_log.get(item_id=log_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return UserLogRead.from_orm(instance)

    @router.patch(
        '/users/{user_id}/roles',
        name=APIAccess.PRIVATE,
        summary='使用者加入多個角色',
        status_code=status.HTTP_200_OK,
        tags=['使用者'],
        dependencies=[Depends(authorize_api)],
    )
    async def update_user_to_roles(
            self,
            role_ids: list[UUID],
            user_id: UUID
    ) -> UserDetailRead:
        role_list = await crud_role.get_by_ids(list_ids=role_ids)
        instance = await crud_user.get(item_id=user_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_user.update_user_to_roles(user=instance, role_list=role_list)
        return instance


router.include_router(
    fastapi_users.get_users_router(UserDetailRead, UserUpdate),
    prefix='/users',
    tags=['使用者'],
)
