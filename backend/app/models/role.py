from sqlmodel import Field, Relationship

from app.models.base import (
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
    SQLModel,
)
from app.models.link import ApiLinkModel, FrontendLinkModel, RoleLinkModel


class RoleBase(SQLModel):
    name: str = Field(
        title='角色名字',
        description='角色名字',
        max_length=32,
        unique=True,
    )


class RoleModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    RoleBase,
    BaseUUIDModel,
    table=True,
):
    is_protected: bool = Field(default=False, description='受保護不可刪除')
    api_list: list['ApiLinkModel'] = Relationship(  # type: ignore
        back_populates='role',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    user_list: list['RoleLinkModel'] = Relationship(  # type: ignore
        back_populates='role',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    frontend_list: list['FrontendLinkModel'] = Relationship(  # type: ignore
        back_populates='role',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
