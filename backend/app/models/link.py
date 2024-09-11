from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base import BaseCreatedAtModel, BaseUUIDModel, SQLModel


class ApiLinkBase(BaseUUIDModel):
    api_id: UUID = Field(
        title='Api ID',
        description='Api ID',
        foreign_key='Api.id',
        primary_key=True,
    )
    role_id: UUID = Field(
        title='角色 ID',
        description='角色 ID',
        foreign_key='Role.id',
        primary_key=True,
    )


class ApiLinkModel(BaseCreatedAtModel, ApiLinkBase, table=True):
    __table_args__ = {
        'comment': 'Api, Role',
    }

    api: 'ApiModel' = Relationship(
        back_populates='role_list',
    )
    role: 'RoleModel' = Relationship(
        back_populates='api_list',
    )


class FrontendLinkBase(BaseUUIDModel, SQLModel):
    frontend_id: UUID = Field(
        title='Frontend ID',
        description='Frontend ID',
        foreign_key='Frontend.id',
        primary_key=True,
    )
    role_id: UUID = Field(
        title='角色 ID',
        description='角色 ID',
        foreign_key='Role.id',
        primary_key=True,
    )


class FrontendLinkModel(BaseCreatedAtModel, FrontendLinkBase, table=True):
    __table_args__ = {
        'comment': 'Frontend, Role',
    }

    frontend: 'FrontendModel' = Relationship(  # type: ignore
        back_populates='role_list',
    )
    role: 'RoleModel' = Relationship(  # type: ignore
        back_populates='frontend_list',
    )


class RoleLinkBase(BaseUUIDModel, SQLModel):
    user_id: UUID = Field(
        title='User ID',
        description='User ID ID',
        foreign_key='User.id',
        primary_key=True,
    )
    role_id: UUID = Field(
        title='Role ID',
        description='Role ID',
        foreign_key='Role.id',
        primary_key=True,
    )


class RoleLinkModel(BaseCreatedAtModel, RoleLinkBase, table=True):
    __table_args__ = {
        'comment': 'Role, User',
    }

    user: 'UserModel' = Relationship(  # type: ignore
        back_populates='role_list',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    role: 'RoleModel' = Relationship(  # type: ignore
        back_populates='user_list',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
