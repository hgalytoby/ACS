from typing import Optional
from pydantic import UUID4
from sqlalchemy import String
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship, Column

from app.models.base import (
    SQLModel,
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
)
from app.models.link import ApiLinkModel
from app.utils.enums import ApiMethod


class ApiGroupBase(SQLModel):
    name: str = Field(
        title='Api 分组名字',
        description='Api 分组名字',
        max_length=32,
        nullable=False,
        unique=True,
    )


class ApiGroupModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    BaseUUIDModel,
    ApiGroupBase,
    table=True,
):
    api_list: list['ApiModel'] = Relationship(  # type: ignore
        back_populates='group',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )


class ApiBase(SQLModel):
    group_id: Optional[UUID4] = Field(
        default=None,
        title='群組 ID',
        description='群組 ID',
        foreign_key='ApiGroup.id',
        nullable=True,
    )


class ApiModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    BaseUUIDModel,
    ApiBase,
    table=True,
):
    uri: str = Field(
        title='Api',
        description='Api',
        max_length=128,
        nullable=False,
    )
    method: ApiMethod = Field(
        title='Api method',
        description='Api method',
        max_length=8,
        nullable=False,
        sa_column=Column(ChoiceType(ApiMethod, impl=String())),
    )
    description: str = Field(
        title='描述',
        description='描述',
        max_length=32,
        nullable=False,
    )
    role_list: list['RoleModel'] = Relationship(  # type: ignore
        back_populates='api_list',
        link_model=ApiLinkModel,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    group: 'ApiGroupModel' = Relationship(
        back_populates='api_list',
    )
