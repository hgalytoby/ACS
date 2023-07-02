from typing import TYPE_CHECKING

from app.models import UserBase, RoleBase, FrontendBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseUpdatedAtRead
from app.utils.partial import optional

if TYPE_CHECKING:
    from .api import ApiRead


class RoleRead(BaseCreatedAtRead, BaseUpdatedAtRead, RoleBase, BaseUUIDRead):
    ...


class RoleApiRead(RoleBase, BaseUUIDRead):
    api_ids: list['ApiRead']


class RoleDetailRead(RoleApiRead, RoleRead):
    user_ids: list[UserBase]
    frontend_ids: list[FrontendBase]


class RoleCreate(RoleBase):
    ...


@optional
class RoleUpdate(RoleBase):
    ...
