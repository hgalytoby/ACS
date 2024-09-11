from datetime import datetime
from uuid import UUID, uuid4

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.orm import declared_attr
from sqlmodel import (
    Field,
    SQLModel as _SQLModel,
)


class SQLModel(_SQLModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
        alias_generator=to_camel,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.replace('Model', '')


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
