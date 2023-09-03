from pydantic import Field

from app.models import LogBase, UserLogBase, SystemLogBase, UserBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead
from app.utils.enums import UserLogEvent
from app.utils.partial import optional


class UserLogCreate(UserLogBase):
    ...


class UserLogRead(LogBase, BaseCreatedAtRead, BaseUUIDRead):
    event: UserLogEvent = Field(
        title='事件類型',
        description='事件類型',
    )


class UserWithLogRead(BaseCreatedAtRead, UserBase, BaseUUIDRead):
    ...


class AllUserLogRead(UserLogRead):
    user: UserWithLogRead


@optional
class UserLogUpdate(UserLogBase):
    ...


class SystemLogCreate(SystemLogBase):
    ...


class SystemLogRead(SystemLogBase):
    ...


@optional
class SystemLogUpdate(LogBase):
    ...
