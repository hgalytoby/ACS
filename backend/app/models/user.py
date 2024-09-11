from fastapi_users_db_sqlmodel import SQLModelBaseOAuthAccount
from humps import kebabize
from pydantic import UUID4
from sqlmodel import Field, Relationship

from app.models.base import (
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
    SQLModel,
)
from app.models.link import RoleLinkModel


class UserBase(SQLModel):
    email: str = Field(
        title='信箱',
        description='信箱',
        max_length=320,
        unique=True,
        index=True,
        nullable=False,
    )
    is_active: bool = Field(
        title='啟用',
        description='啟用',
        default=True,
        nullable=False,
    )
    is_superuser: bool = Field(
        title='超級使用者',
        description='超級使用者',
        default=False,
        nullable=False,
    )
    is_verified: bool = Field(
        title='驗證',
        description='驗證',
        default=False,
        nullable=False,
    )
    username: str = Field(
        title='使用者名字',
        description='使用者名字',
        max_length=64,
        nullable=False,
        default_factory=str,
    )

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                'id',
                'is_superuser',
                'is_active',
                'is_verified',
                'oauth_accounts',
                'avatar',
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={'id', 'avatar'})


class UserModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    UserBase,
    BaseUUIDModel,
    table=True,
):
    hashed_password: str = Field(
        title='密碼',
        description='密碼',
        max_length=1024,
        nullable=False,
    )
    oauth_accounts: list['OAuthAccountModel'] = Relationship(  # type: ignore
        back_populates='user',
        sa_relationship_kwargs={
            'lazy': 'joined',
        },
    )
    avatar: str = Field(
        default='',
        title='頭像',
        description='頭像',
        nullable=True,
        max_length=128,
    )
    log_list: list['UserLogModel'] = Relationship(  # type: ignore
        back_populates='user',
        # sa_relationship_kwargs={
        #     'lazy': 'selectin',
        # }
    )
    role_list: list[RoleLinkModel] = Relationship(  # type: ignore
        back_populates='user',
        sa_relationship_kwargs={
            'lazy': 'joined',
        },
    )

    def get_file_value(self) -> str:
        return self.avatar

    def get_folder_name(self) -> str:
        return kebabize(self.__tablename__)

    def set_file_value(self, value: str):
        self.avatar = value


class OAuthAccountModel(BaseUUIDModel, SQLModelBaseOAuthAccount, table=True):
    user_id: UUID4 = Field(
        title='使用者 ID',
        description='使用者 ID',
        foreign_key='User.id',
        nullable=False,
    )
    user: 'UserModel' = Relationship(
        back_populates='oauth_accounts',
        # sa_relationship_kwargs={
        #     'lazy': 'joined',
        # },
    )
