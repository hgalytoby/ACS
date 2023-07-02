from app.crud.base import CRUDBase
from app.models import RoleModel, UserModel, ApiModel
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead, RoleDetailRead


class CRUDRole(CRUDBase[RoleModel, RoleCreate, RoleUpdate, RoleRead]):
    async def update_user_ids(
            self,
            *,
            role: RoleModel,
            users: list[UserModel],
    ) -> RoleDetailRead:
        role.user_ids = users
        self.db.session.add(role)
        await self.db.session.commit()
        await self.db.session.refresh(role)
        return RoleDetailRead.from_orm(role)

    async def update_api_ids(
            self,
            *,
            role: RoleModel,
            apis: list[ApiModel],
    ) -> RoleDetailRead:
        role.api_ids = apis
        self.db.session.add(role)
        await self.db.session.commit()
        await self.db.session.refresh(role)
        return RoleDetailRead.from_orm(role)


crud_role = CRUDRole(model=RoleModel)
