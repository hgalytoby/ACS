from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import RoleModel, UserModel, ApiModel, FrontendModel
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleRead,
    RoleFrontendRead,
    RoleUserRead, RoleApiRead,
)


class CRUDRole(CRUDBase[RoleModel, RoleCreate, RoleUpdate, RoleRead]):
    async def update_user_ids(
            self,
            *,
            role: RoleModel,
            users: list[UserModel],
            db_session: Optional[AsyncSession] = None,
    ) -> RoleUserRead:
        db_session = db_session or self.db.session
        role.user_ids = users
        instance = await self.save(instance=role, db_session=db_session)
        return RoleUserRead.from_orm(instance)

    async def update_api_ids(
            self,
            *,
            role: RoleModel,
            apis: list[ApiModel],
            db_session: Optional[AsyncSession] = None,
    ) -> RoleApiRead:
        db_session = db_session or self.db.session
        role.api_ids = apis
        instance = await self.save(instance=role, db_session=db_session)
        return RoleApiRead.from_orm(instance)

    async def update_role_to_frontends(
            self,
            *,
            role: RoleModel,
            frontend_list: list[FrontendModel],
            db_session: Optional[AsyncSession] = None,
    ) -> RoleFrontendRead:
        db_session = db_session or self.db.session
        role.frontend_ids = frontend_list
        instance = await self.save(instance=role, db_session=db_session)
        return RoleFrontendRead.from_orm(instance)


crud_role = CRUDRole(model=RoleModel)
