from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field
from typing import TYPE_CHECKING

from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseModel, BaseUpdatedAtRead
from app.models import UserBase
from app.utils.partial import optional

if TYPE_CHECKING:
    from .role import RoleFrontendRead


class UserRead(BaseUpdatedAtRead, BaseCreatedAtRead, UserBase, BaseUUIDRead):
    last_login: datetime = Field(
        title='',
        description='',
    )


class UserDetailRead(UserRead):
    role_ids: list['RoleFrontendRead'] = Field(default_factory=list, description='角色')


class UserCreate(UserBase):
    email: EmailStr = Field(description='信箱', title='信箱')
    password: str = Field(min_length=8, description='密碼', title='密碼')


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


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(title='舊密碼', min_length=6, max_length=32)
    new_password: str = Field(title='新密碼', min_length=6, max_length=32)
