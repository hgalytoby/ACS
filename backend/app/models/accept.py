from pydantic import Field

from app.models.base import (
    BaseCreatedAtModel,
    BaseUUIDModel,
    BaseUpdatedAtModel,
    SQLModel,
)


class AcceptApiBase(SQLModel):
    api: str = Field(
        title='Api',
        description='Api',
    )


class AcceptApiModel(
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    AcceptApiBase,
    BaseUUIDModel,
    table=True,
):
    ...
