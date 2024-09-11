from typing import Optional

from pydantic import ConfigDict, Field

from app.models import FrontendBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead, BaseUpdatedAtRead
from app.utils.partial import optional


class FrontendCreate(FrontendBase):
    parent_id: Optional[str] = Field(default=None)


class FrontendRead(
    BaseCreatedAtRead,
    BaseUpdatedAtRead,
    FrontendBase,
    BaseUUIDRead,
):
    depth: int = Field(
        title='深度',
        description='深度',
    )
    children: list['FrontendRead'] = Field(
        default_factory=list,
        title='小孩',
        description='小孩',
    )


@optional()
class FrontendUpdate(FrontendBase):
    ...
