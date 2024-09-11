from uuid import UUID

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import ChoiceType
from sqlmodel import Column, Field, Relationship

from app.models.base import BaseCreatedAtModel, BaseUUIDModel
from app.utils.enums import SystemLogEvent, UserLogEvent


class LogBase(BaseCreatedAtModel, BaseUUIDModel):
    raw_data: dict = Field(
        default_factory=dict,
        title='原始資料',
        description='原始資料',
        sa_type=JSON,
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
