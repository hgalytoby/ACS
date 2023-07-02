from typing import Optional, Generic, TypeVar
from pydantic import Field

from app.schemas.base import BaseModel
from app.utils.enums import WebSocketEvent

DataType = TypeVar('DataType')


class WebSocketEventSchema(BaseModel, Generic[DataType]):
    data: Optional[DataType] = Field(default=None, description='資料')
    event: WebSocketEvent = Field(description='事件動作')
