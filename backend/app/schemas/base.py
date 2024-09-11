from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel as _BaseModel,
    ConfigDict,
    Field,
    model_validator,
)
from pydantic.alias_generators import to_camel
import orjson


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        alias_generator=to_camel,
    )


class BaseJsonModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**orjson.loads(value))
        return value


class BaseCreatedAtRead(BaseModel):
    created_at: datetime = Field(
        title='創建時間',
        description='創建時間',
    )


class BaseUpdatedAtRead(BaseModel):
    updated_at: datetime = Field(
        title='更新時間',
        description='更新時間',
    )


class BaseUUIDRead(BaseModel):
    id: UUID = Field(
        title='ID',
        description='ID',
    )
