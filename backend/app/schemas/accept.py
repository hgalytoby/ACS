from pydantic import Field

from app.models import AcceptApiBase
from app.schemas.base import BaseModel
from app.utils.partial import optional


class AcceptApi(BaseModel):
    api: str = Field()


class AcceptApiRead(AcceptApiBase):
    ...


class AcceptApiCreate(AcceptApiBase):
    ...


@optional
class AcceptApiUpdate(AcceptApiBase):
    ...
