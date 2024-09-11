from fastapi import Request
from pydantic import Field, validator

from app.core.config import settings
from app.models import EmailSettingsBase
from app.schemas.base import (
    BaseCreatedAtRead,
    BaseModel,
    BaseUUIDRead,
    BaseUpdatedAtRead,
)
from app.utils.enums import SystemLogEvent
from app.utils.partial import optional

domain = settings.domain


class EmailSettingsCreate(EmailSettingsBase):
    ...


class EmailSettingsRead(
    BaseCreatedAtRead,
    EmailSettingsBase,
    BaseUUIDRead,
):
    event: SystemLogEvent = Field(
        title='事件類型',
        description='事件類型',
    )


@optional()
class EmailSettingsUpdate(EmailSettingsBase):
    ...


class EmailSendCreate(BaseModel):
    subject: str
    email: str
    body: str


class EmailTrySendSchema(BaseModel):
    subject: str
    body: str
    event: SystemLogEvent = Field(
        title='事件類型',
        description='事件類型',
    )

    def get_sample_body(self, request: Request) -> str:
        match self.event:
            case SystemLogEvent.USER_FORGOT_PASSWORD:
                return self.body.replace(
                    '{url}',
                    f'{domain}/auth/verify?token=123',
                )
            case SystemLogEvent.USER_REGISTER:
                return self.body.replace(
                    '{url}',
                    f'{domain}/auth/reset-password?token=123',
                )
            case SystemLogEvent.USER_LOGIN_FAIL:
                return self.body.replace('{ip}', request.client.host)
            case _:
                return self.body

    @validator('event', pre=True)
    def _event(cls, v: str, values: dict):
        if v in {
            SystemLogEvent.USER_REGISTER.value,
            SystemLogEvent.USER_FORGOT_PASSWORD.value,
        }:
            cls.validate_body_format(values=values, format_string='{url}')
        elif v == SystemLogEvent.USER_LOGIN_FAIL.value:
            cls.validate_body_format(values=values, format_string='{ip}')
        return v

    @classmethod
    def validate_body_format(cls, values: dict, format_string: str):
        body = values.get('body', '')
        if format_string not in body:
            raise ValueError(f'{format_string} not in body')
        if body.count(format_string) > 1:
            raise ValueError(f'{format_string} count > 1')
