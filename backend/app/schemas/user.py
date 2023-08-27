from datetime import datetime

import orjson
from pydantic import EmailStr
from sqlmodel import Field
from typing import TYPE_CHECKING

from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseModel, BaseUpdatedAtRead
from app.models import UserBase
from app.utils.partial import optional

if TYPE_CHECKING:
    from .role import RoleFrontendListRead


class UserRead(BaseUpdatedAtRead, BaseCreatedAtRead, UserBase, BaseUUIDRead):
    avatar: str = Field(
        title='頭像',
        description='頭像',
    )


class OAuthAccountsRead(BaseUUIDRead):
    oauth_name: str = Field(description='第三方名稱', title='第三方名稱')


class UserDetailRead(UserRead):
    role_list: list['RoleFrontendListRead'] = Field(
        default_factory=list,
        description='角色',
        title='角色',
    )
    oauth_accounts: list[OAuthAccountsRead] = Field(
        default_factory=list,
        description='第三方帳號',
        title='第三方帳號',
    )


class UserCreate(UserBase):
    email: EmailStr = Field(description='信箱', title='信箱')
    password: str = Field(
        min_length=8,
        max_length=64,
        description='密碼',
        title='密碼',
    )


@optional
class UserUpdate(UserCreate):
    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                'id',
                'is_superuser',
                'is_active',
                'is_verified',
                'oauth_accounts',
                'email',
                'avatar',
            },
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**orjson.loads(value))
        return value


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(
        description='舊密碼',
        title='舊密碼',
        min_length=8,
        max_length=32,
    )
    new_password: str = Field(
        description='舊密碼',
        title='新密碼',
        min_length=8,
        max_length=32,
    )


class OAuthAccountCreate(BaseModel):
    ...


class OAuthAccountUpdate(BaseModel):
    ...


class OAuthAccountRead(BaseModel):
    ...
