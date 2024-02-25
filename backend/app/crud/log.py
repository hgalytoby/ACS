from sqlalchemy.orm import joinedload
from sqlmodel import func, select
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.crud.base import CRUDBase
from app.models import SystemLogModel, UserLogModel
from app.schemas.log import (
    AllUserLogRead,
    SystemLogCreate,
    SystemLogRead,
    SystemLogUpdate,
    UserLogCreate,
    UserLogRead,
    UserLogUpdate,
)
from app.utils.enums import SystemLogEvent


class CRUDUserLog(
    CRUDBase[
        UserLogModel,
        UserLogCreate,
        UserLogUpdate,
        UserLogRead | AllUserLogRead,
    ]
):
    def get_select(self) -> Select | SelectOfScalar:
        return (
            select(self.model)
            .options(joinedload(self.model.user))
            .join(self.model.user)
        )


class CRUDSystemLog(
    CRUDBase[
        SystemLogModel,
        SystemLogCreate,
        SystemLogUpdate,
        SystemLogRead,
    ]
):
    async def chart(self) -> list[tuple[SystemLogEvent, int]]:
        response = await self.db.session.execute(
            select(
                self.model.event,
                func.count(self.model.event),
            ).group_by(self.model.event),
        )
        return response.all()


crud_user_log = CRUDUserLog(model=UserLogModel)
crud_system_log = CRUDSystemLog(model=SystemLogModel)
