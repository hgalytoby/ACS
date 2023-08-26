from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship, Column
from app.models.base import SQLModel, BaseCreatedAtModel, BaseUUIDModel
from uuid import UUID

from app.utils.enums import UserLogEvent, SystemLogEvent


class LogBase(BaseCreatedAtModel, BaseUUIDModel, SQLModel):
    raw_data: dict = Field(
        default_factory=dict,
        title='原始資料',
        description='原始資料',
        sa_column=Column(JSON),
    )


class SystemLogBase(LogBase):
    event: SystemLogEvent = Field(
        title='事件類型',
        description='事件類型',
        sa_column=Column(ChoiceType(SystemLogEvent, impl=String())),
    )


class UserLogBase(LogBase):
    user_id: UUID = Field(foreign_key='User.id')
    event: UserLogEvent = Field(
        title='事件類型',
        description='事件類型',
        sa_column=Column(ChoiceType(UserLogEvent, impl=String())),
    )


class SystemLogModel(SystemLogBase, table=True):
    ...


class UserLogModel(UserLogBase, table=True):
    user: 'UserModel' = Relationship(  # type: ignore
        back_populates='log_list',
    )
