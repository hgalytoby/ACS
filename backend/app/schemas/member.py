from typing import Optional
from uuid import UUID

from pydantic import Field, model_validator, validator
import orjson

from app.core.config import settings
from app.models import (
    MemberBase,
    MemberLocationBase,
    MemberRecordBase,
    MemberStatusBase,
)
from app.schemas.base import (
    BaseCreatedAtRead,
    BaseJsonModel,
    BaseModel,
    BaseUUIDRead,
    BaseUpdatedAtRead,
)
from app.utils.partial import optional


class MemberLocationCreate(MemberLocationBase, BaseJsonModel):
    ...


class MemberLocationRead(
    BaseCreatedAtRead,
    BaseUpdatedAtRead,
    MemberLocationBase,
    BaseUUIDRead,
):
    image: str = Field(
        description='圖片網址',
        title='圖片網址',
    )


@optional()
class MemberLocationUpdate(MemberLocationCreate):
    ...


class MemberCreate(MemberBase, BaseJsonModel):
    ...


class MemberRead(
    BaseCreatedAtRead,
    BaseUpdatedAtRead,
    MemberBase,
    BaseUUIDRead,
):
    image: str = Field(description='圖片', title='圖片')
    qrcode: str = Field(description='Qrcode', title='Qrcode')


class MemberDetailRead(MemberRead):
    member_status: Optional['MemberStatusRead'] = Field(
        description='成員狀態',
        title='成員狀態',
        alias='member_status_id',
    )


@optional()
class MemberUpdate(MemberCreate):
    ...


class MemberRecordCreate(MemberRecordBase):
    ...


class MemberRecordRead(
    BaseCreatedAtRead,
    MemberRecordBase,
    BaseUUIDRead,
):
    ...


@optional()
class MemberRecordUpdate(MemberRecordBase):
    ...


class MemberStatusCreate(MemberStatusBase):
    member_id: UUID = Field(
        title='成員ID',
        description='成員ID',
    )
    member_location_id: UUID = Field(
        title='地點ID',
        description='地點ID',
    )
    project: str

    @validator('project', pre=True)
    def _project(cls, v):
        if settings.project != v:
            raise ValueError('project error')
        return v


class MemberStatusRead(BaseModel):
    member_location: MemberLocationRead = Field(
        description='成員地點',
        title='成員地點',
    )
    member_list: list[MemberRead] = Field(
        description='成員資料',
        title='成員資料',
    )


class MemberStatusCreatedRead(BaseCreatedAtRead):
    status: bool = Field(description='狀態', title='狀態')
    member: MemberRead = Field(description='成員資料', title='成員資料')
    member_location: MemberLocationRead = Field(
        description='成員地點',
        title='成員地點',
    )


@optional()
class MemberStatusUpdate(MemberStatusBase):
    ...
