from datetime import date
from uuid import UUID
from humps import kebabize
from sqlmodel import Field, Relationship
from typing import Optional

from app.models.base import (
    SQLModel,
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
)
from app.utils.enums import BloodType


class MemberLocationBase(SQLModel):
    name: str = Field(
        title='名字',
        description='名字',
        max_length=64,
        unique=True,
        nullable=False,
    )


class MemberLocationModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    MemberLocationBase,
    BaseUUIDModel,
    table=True,
):
    image: str = Field(
        title='圖片',
        description='圖片',
        max_length=256,
        default=None,
        nullable=True,
    )
    member_status_id: list['MemberStatusModel'] = Relationship(  # type: ignore
        back_populates='member_location',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete',
            'passive_deletes': True,
        },
    )

    def get_file_value(self) -> str:
        return self.image

    def get_folder_name(self) -> str:
        return kebabize(self.__tablename__)

    def set_file_value(self, value: str):
        self.image = value


class MemberBase(SQLModel):
    name: str = Field(
        title='名字',
        description='名字',
        max_length=32,
        nullable=False,
    )
    blood_type: BloodType = Field(
        title='血型',
        description='血型',
        nullable=False,
    )
    birthday: date = Field(
        title='生日',
        description='生日',
        nullable=False,
    )
    phone: str = Field(
        title='手機號碼',
        description='手機號碼',
        nullable=False,
        regex=r'09\d{8}$',
        unique=True
    )
    company: str = Field(
        title='公司',
        description='公司',
        max_length=32,
        nullable=False,
    )
    job_title: str = Field(
        title='職稱',
        description='職稱',
        max_length=32,
        nullable=False,
    )


class MemberModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    MemberBase,
    BaseUUIDModel,
    table=True,
):
    image: str = Field(
        title='圖片',
        description='圖片',
        max_length=256,
        default=None,
        nullable=True,
    )
    qrcode: str = Field(
        title='Qrcode',
        description='Qrcode',
        max_length=256,
        default=None,
        nullable=True,
    )
    member_status_id: Optional['MemberStatusModel'] = Relationship(
        back_populates='member',
        sa_relationship_kwargs={
            'lazy': 'selectin',
            'cascade': 'all, delete',
            'passive_deletes': True,
        },
    )

    def get_file_value(self) -> str:
        return self.image

    def get_folder_name(self) -> str:
        return kebabize(self.__tablename__)

    def set_file_value(self, value: str):
        self.image = value

    def get_qrcode_value(self) -> str:
        return self.qrcode

    def set_qrcode_value(self, value):
        self.qrcode = value


class MemberRecordBase(SQLModel):
    status: bool = Field(
        title='狀態',
        description='狀態',
        nullable=False,
    )
    member_location_id: UUID = Field(
        title='成員 ID',
        description='成員 ID',
    )
    member_location_name: str = Field(
        title='地點名字',
        description='地點名字',
        max_length=64,
        nullable=False,
    )
    member_location_image: str = Field(
        title='地點圖片',
        description='地點圖片',
        max_length=256,
        default=None,
        nullable=True,
    )
    member_id: UUID = Field(
        title='成員 ID',
        description='成員 ID',
    )
    member_name: str = Field(
        title='成員名字',
        description='成員名字',
        max_length=32,
        nullable=False,
    )
    member_phone: str = Field(
        title='成員手機號碼',
        description='成員手機號碼',
        nullable=False,
        regex=r'09\d{8}$',
    )
    member_company: str = Field(
        title='成員公司',
        description='成員公司',
        max_length=32,
        nullable=False,
    )
    member_job_title: str = Field(
        title='成員職稱',
        description='成員職稱',
        max_length=32,
        nullable=False,
    )
    member_image: str = Field(
        title='成員圖片',
        description='成員圖片',
        max_length=256,
        default=None,
        nullable=True,
    )


class MemberRecordModel(
    BaseCreatedAtModel,
    MemberRecordBase,
    BaseUUIDModel,
    table=True,
):
    ...


class MemberStatusBase(SQLModel):
    status: bool = Field(
        title='狀態',
        description='狀態',
        nullable=False,
    )


class MemberStatusModel(
    BaseCreatedAtModel,
    MemberStatusBase,
    BaseUUIDModel,
    table=True,
):
    member_id: UUID = Field(
        title='成員ID',
        description='成員ID',
        foreign_key='Member.id',
    )
    member_location_id: UUID = Field(
        title='地點ID',
        description='地點ID',
        foreign_key='MemberLocation.id',
    )
    member: 'MemberModel' = Relationship(
        back_populates='member_status_id',
        sa_relationship_kwargs={
            'uselist': False,
        },
    )
    member_location: 'MemberLocationModel' = Relationship(
        back_populates='member_status_id',
    )
