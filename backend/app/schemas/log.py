from app.models import LogBase, UserLogBase, SystemLogBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead
from app.utils.partial import optional


class UserLogCreate(UserLogBase):
    ...


class UserLogRead(LogBase, BaseCreatedAtRead, BaseUUIDRead):
    ...


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
