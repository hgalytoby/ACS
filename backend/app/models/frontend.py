from typing import Optional
from uuid import UUID
from sqlmodel import Field, Relationship

from app.models import FrontendLinkModel
from app.models.base import (
    BaseCreatedAtModel,
    BaseUUIDModel,
    SQLModel,
    BaseUpdatedAtModel,
)


class FrontendBase(SQLModel):
    description: str = Field(
        title='描述',
        description='描述',
        max_length=32,
        nullable=False,
    )
    value: str = Field(
        title='値',
        description='値',
        max_length=32,
        nullable=False,
    )
    parent_id: Optional[UUID] = Field(
        foreign_key='Frontend.id',
        default=None,
        nullable=True
    )


class FrontendModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    BaseUUIDModel,
    FrontendBase,
    table=True,
):
    depth: int = Field(
        default=1,
        title='深度',
        description='深度',
    )
    role_list: list['RoleModel'] = Relationship(  # type: ignore
        back_populates='frontend_list',
        link_model=FrontendLinkModel,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    parent: Optional['FrontendModel'] = Relationship(
        back_populates='children',
        sa_relationship_kwargs=dict(
            remote_side='FrontendModel.id'  # notice the uppercase "N" to refer to this table class
        )
    )
    children: list['FrontendModel'] = Relationship(
        back_populates='parent',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
