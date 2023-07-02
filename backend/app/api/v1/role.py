from uuid import UUID
from fastapi import status, HTTPException, Query, APIRouter
from fastapi_restful.cbv import cbv

from app.crud import crud_role, crud_user, crud_api
from app.schemas.role import RoleRead, RoleCreate, RoleUpdate, RoleDetailRead
from app.utils.enums import APIAccess

router = APIRouter()


@cbv(router)
class UserRoleView:
    @router.get(
        '/roles',
        name=APIAccess.PRIVATE,
        summary='角色列表',
        status_code=status.HTTP_200_OK,
        tags=['角色'],
    )
    async def get_multi(self) -> list[RoleRead]:
        return await crud_role.get_multi()

    @router.post(
        '/roles',
        name=APIAccess.PRIVATE,
        summary='新增角色',
        status_code=status.HTTP_201_CREATED,
        tags=['角色'],
    )
    async def create(self, item: RoleCreate) -> RoleRead:
        instance = await crud_role.create(create_item=item)
        return instance

    @router.patch(
        '/roles/{role_id}/user-ids',
        name=APIAccess.PRIVATE,
        summary='角色批量更新使用者',
        status_code=status.HTTP_200_OK,
        tags=['角色'],
    )
    async def update_user_ids(
            self,
            role_id: UUID,
            user_ids: list[UUID],
    ) -> RoleDetailRead:
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
        tags=['角色'],
    )
    async def update_api_ids(
            self,
            role_id: UUID,
            api_ids: list[UUID],
    ) -> RoleDetailRead:
        role = await crud_role.get(item_id=role_id)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        apis = await crud_api.get_by_ids(list_ids=api_ids)
        role = await crud_role.update_api_ids(apis=apis, role=role)
        return role

    # @router.patch(
    #     '/roles/user-add-roles',
    #     name=APIAccess.PRIVATE,
    #     summary='使用者加入多個角色',
    #     status_code=status.HTTP_200_OK,
    #     tags=['角色'],
    # )
    # async def user_add_roles(
    #         self,
    #         user_id: UUID,
    #         roles_ids: list[UUID],
    # ) -> UserDetailRead:
    #     user = await crud_user.get(item_id=user_id)
    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #     user = await crud_role.user_add_roles(user=user, roles_ids=roles_ids)
    #     return user

    @router.get(
        '/roles/{role_id}',
        name=APIAccess.PRIVATE,
        summary='單筆角色資料',
        status_code=status.HTTP_200_OK,
        tags=['角色'],
    )
    async def get(
            self,
            role_id: UUID,
            detail: bool = Query(default=False),
    ) -> RoleDetailRead | RoleRead:
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
        tags=['角色'],
    )
    async def update(self, role_id: UUID, item: RoleUpdate) -> RoleRead:
        instance = await crud_role.get(item_id=role_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_role.update(current_item=instance, update_item=item)
        return instance

    @router.delete(
        '/roles/{role_id}',
        name=APIAccess.PRIVATE,
        summary='刪除角色資料',
        status_code=status.HTTP_204_NO_CONTENT,
        tags=['角色'],
    )
    async def destroy(self, role_id: UUID):
        instance = await crud_role.get(item_id=role_id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await crud_role.destroy(item_id=instance.id)
