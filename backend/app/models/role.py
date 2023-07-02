from sqlmodel import Field, Relationship

from app.models.base import (
    SQLModel,
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
)
from app.models.link import ApiLinkModel, RoleLinkModel, FrontendLinkModel


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
    api_ids: list['ApiModel'] = Relationship(  # type: ignore
        back_populates='role_ids',
        link_model=ApiLinkModel,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    user_ids: list['UserModel'] = Relationship(  # type: ignore
        back_populates='role_ids',
        link_model=RoleLinkModel,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
    frontend_ids: list['FrontendModel'] = Relationship(  # type: ignore
        back_populates='role_ids',
        link_model=FrontendLinkModel,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )
