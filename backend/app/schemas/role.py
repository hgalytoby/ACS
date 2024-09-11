from typing import TYPE_CHECKING

from pydantic import Field

from app.models import FrontendBase, RoleBase, UserBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseUpdatedAtRead
from app.utils.partial import optional

if TYPE_CHECKING:
    from .api import ApiRead


class RoleRead(BaseCreatedAtRead, BaseUpdatedAtRead, RoleBase, BaseUUIDRead):
    ...


class RoleApiRead(RoleBase, BaseUUIDRead):
    api_list: list['ApiRead'] = Field(
        default_factory=list,
        description='API',
        title='API',
    )


class RoleFrontendRead(FrontendBase, BaseUUIDRead):
    ...


class RoleFrontendListRead(RoleBase):
    frontend_list: list[RoleFrontendRead] = Field(
        default_factory=list,
        description='前端',
        title='前端',
    )


class RoleUserRead(RoleBase, BaseUUIDRead):
    user_list: list[UserBase] = Field(
        default_factory=list,
        description='使用者',
        title='使用者',
    )


class RoleDetailRead(RoleFrontendListRead, RoleUserRead, RoleApiRead):
    ...


class RoleCreate(RoleBase):
    ...


@optional()
class RoleUpdate(RoleBase):
    ...
