from pydantic import Field

from app.core.config import settings
from app.schemas.base import BaseModel


class HealthRead(BaseModel):
    project: str = Field(
        default=settings.project,
        description='專案名稱',
        title='專案名稱',
    )


health_read = HealthRead()
