from sqlalchemy import String
from sqlalchemy_utils import ChoiceType
from sqlmodel import Column, Field

from app.models.base import (
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
    SQLModel,
)
from app.utils.enums import SystemLogEvent


class EmailSettingsBase(SQLModel):
    subject: str = Field(
        title='主題',
        description='主題',
        nullable=False,
    )
    body: str = Field(
        title='內容',
        description='內容',
        nullable=False,
    )


class EmailSettingsModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    EmailSettingsBase,
    BaseUUIDModel,
    table=True,
):
    event: SystemLogEvent = Field(
        unique=True,
        title='事件類型',
        description='事件類型',
        sa_column=Column(ChoiceType(SystemLogEvent, impl=String())),
    )
