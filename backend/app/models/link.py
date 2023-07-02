from uuid import UUID
from app.models.base import SQLModel, BaseUUIDModel, BaseCreatedAtModel
from sqlmodel import Field, Relationship


class ApiLinkBase(BaseUUIDModel, SQLModel):
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

    api: 'ApiModel' = Relationship(  # type: ignore
        back_populates='role_ids',
    )
    role: 'RoleModel' = Relationship(  # type: ignore
        back_populates='api_ids',
    )


class ApiLinkModel(BaseCreatedAtModel, ApiLinkBase, table=True):
    __table_args__ = {
        'comment': 'Api, Role',
    }


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
    frontend: 'FrontendModel' = Relationship(  # type: ignore
        back_populates='role_ids',
    )
    role: 'RoleModel' = Relationship(  # type: ignore
        back_populates='frontend_ids',
    )


class FrontendLinkModel(BaseCreatedAtModel, FrontendLinkBase, table=True):
    __table_args__ = {
        'comment': 'Frontend, Role',
    }


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

    user: 'UserModel' = Relationship(  # type: ignore
        back_populates='role_ids',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    role: 'RoleModel' = Relationship(  # type: ignore
        back_populates='user_ids',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )


class RoleLinkModel(BaseCreatedAtModel, RoleLinkBase, table=True):
    __table_args__ = {
        'comment': 'Role, User',
    }
