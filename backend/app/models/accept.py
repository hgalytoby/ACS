from pydantic import Field

from app.models.base import (
    SQLModel,
    BaseCreatedAtModel,
    BaseUpdatedAtModel,
    BaseUUIDModel,
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
