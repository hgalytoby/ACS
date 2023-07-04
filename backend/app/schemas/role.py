from typing import TYPE_CHECKING

from pydantic import Field

from app.models import UserBase, RoleBase, FrontendBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseUpdatedAtRead
from app.utils.partial import optional

if TYPE_CHECKING:
    from .api import ApiRead


class RoleRead(BaseCreatedAtRead, BaseUpdatedAtRead, RoleBase, BaseUUIDRead):
    ...


class RoleApiRead(RoleBase, BaseUUIDRead):
    api_ids: list['ApiRead'] = Field(default_factory=list, description='API', title='API')


class RoleFrontendRead(RoleBase, BaseUUIDRead):
    frontend_ids: list[FrontendBase] = Field(default_factory=list, description='前端', title='前端')


class RoleUserRead(RoleBase, BaseUUIDRead):
    user_ids: list[UserBase] = Field(default_factory=list, description='使用者', title='使用者')


class RoleDetailRead(RoleFrontendRead, RoleUserRead, RoleApiRead):
    ...


class RoleCreate(RoleBase):
    ...


@optional
class RoleUpdate(RoleBase):
    ...
