from datetime import datetime
from uuid import UUID
from pydantic import BaseModel as _BaseModel, Field
from humps import camelize

from app.utils.json import Json


class BaseModel(_BaseModel):
    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        alias_generator = (lambda string: camelize(string))
        allow_population_by_field_name = True
        json_dumps = Json.dumps
        json_loads = Json.loads


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
