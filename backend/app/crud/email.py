from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import EmailSettingsModel
from app.schemas.email import (
    EmailSettingsCreate,
    EmailSettingsUpdate,
    EmailSettingsRead,
)
from app.utils.enums import SystemLogEvent


class CRUDEmailSettings(
    CRUDBase[
        EmailSettingsModel,
        EmailSettingsCreate,
        EmailSettingsUpdate,
        EmailSettingsRead,
    ],
):
    async def get_event(
            self,
            *,
            event: SystemLogEvent,
            db_session: Optional[AsyncSession] = None,
    ) -> Optional[EmailSettingsModel]:
        db_session = db_session or self.db.session
        query = self.get_select().where(self.model.event == event)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()


crud_email_settings = CRUDEmailSettings(model=EmailSettingsModel)
