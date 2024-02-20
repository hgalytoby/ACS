from datetime import datetime
from uuid import UUID, uuid4

from humps import camelize
from sqlalchemy.orm import declared_attr
from sqlmodel import (
    Field,
    SQLModel as _SQLModel,
)

from app.utils.json import Json


class SQLModel(_SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.replace('Model', '')

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
        alias_generator = (lambda string: camelize(string))
        allow_population_by_field_name = True
        json_dumps = Json.dumps
        json_loads = Json.loads


class BaseCreatedAtModel(SQLModel):
    created_at: datetime = Field(
        title='創建時間',
        description='創建時間',
        default_factory=datetime.utcnow,
        nullable=False,
    )


class BaseUpdatedAtModel(SQLModel):
    updated_at: datetime | None = Field(
        title='更新時間',
        description='更新時間',
        default_factory=datetime.utcnow,
        sa_column_kwargs={'onupdate': datetime.utcnow},
    )


class BaseUUIDModel(SQLModel):
    id: UUID = Field(
        title='pk',
        description='pk',
        default_factory=uuid4,
        primary_key=True,
    )
