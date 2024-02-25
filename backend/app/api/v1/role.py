from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_restful.cbv import cbv

from app.crud import crud_api, crud_frontend, crud_role, crud_user
from app.schemas.role import (
    RoleApiRead,
    RoleCreate,
    RoleDetailRead,
    RoleFrontendListRead,
    RoleRead,
    RoleUpdate,
    RoleUserRead,
)
from app.utils.enums import APIAccess

router = APIRouter(tags=['角色'])


@cbv(router)
class UserRoleView:
    @router.get(
        '/roles',
        name=APIAccess.PRIVATE,
        summary='角色列表',
        status_code=status.HTTP_200_OK,
    )
    async def get_multi(self) -> list[RoleRead]:
        return await crud_role.get_multi()

    @router.post(
        '/roles',
        name=APIAccess.PRIVATE,
        summary='新增角色',
        status_code=status.HTTP_201_CREATED,
    )
    async def create(self, item: RoleCreate) -> RoleRead:
        instance = await crud_role.create(create_item=item)
        return instance

    @router.patch(
        '/roles/{role_id}/user-ids',
        name=APIAccess.PRIVATE,
        summary='角色批量更新使用者',
        status_code=status.HTTP_200_OK,
    )
    async def update_user_ids(
        self,
        role_id: UUID,
        user_ids: list[UUID],
    ) -> RoleUserRead:
        role = await crud_role.get(item_id=role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        users = await crud_user.get_by_ids(list_ids=user_ids)
        role = await crud_role.update_user_ids(users=users, role=role)
        return role

    @router.patch(
        '/roles/{role_id}/api-ids',
        name=APIAccess.PRIVATE,
        summary='角色批量更新 Api',
        status_code=status.HTTP_200_OK,
    )
    async def update_api_ids(
        self,
        role_id: UUID,
        api_ids: list[UUID],
    ) -> RoleApiRead:
        role = await crud_role.get(item_id=role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        apis = await crud_api.get_by_ids(list_ids=api_ids)
        role = await crud_role.update_api_ids(apis=apis, role=role)
        return role

    @router.patch(
        '/roles/{role_id}/frontend-ids',
        name=APIAccess.PRIVATE,
        summary='角色批量更新 Frontend',
        status_code=status.HTTP_200_OK,
    )
    async def update_role_to_frontends(
        self,
        role_id: UUID,
        frontend_ids: list[UUID],
    ) -> RoleFrontendListRead:
        frontend_list = await crud_frontend.get_by_ids(list_ids=frontend_ids)
        role = await crud_role.get(item_id=role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        role = await crud_role.update_role_to_frontends(
            role=role,
            frontend_list=frontend_list,
        )
        return role

    @router.get(
        '/roles/{role_id}',
        name=APIAccess.PRIVATE,
        summary='單筆角色資料',
        status_code=status.HTTP_200_OK,
    )
    async def get(
        self,
        role_id: UUID,
        detail: bool = Query(
            default=False,
            description='詳細資料',
            title='詳細資料',
        ),
    ) -> RoleRead | RoleDetailRead:
        instance = await crud_role.get(item_id=role_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        if detail:
            return RoleDetailRead.from_orm(instance)
        return RoleRead.from_orm(instance)

    @router.patch(
        '/roles/{role_id}',
        name=APIAccess.PRIVATE,
        summary='更新角色資料',
        status_code=status.HTTP_200_OK,
    )
    async def update(self, role_id: UUID, item: RoleUpdate) -> RoleRead:
        instance = await crud_role.get(item_id=role_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_role.update(
            current_item=instance,
            update_item=item,
        )
        return instance

    @router.delete(
        '/roles/{role_id}',
        name=APIAccess.PRIVATE,
        summary='刪除角色資料',
        status_code=status.HTTP_204_NO_CONTENT,
    )
    async def destroy(self, role_id: UUID):
        instance = await crud_role.get(item_id=role_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await crud_role.destroy(item_id=instance.id)
