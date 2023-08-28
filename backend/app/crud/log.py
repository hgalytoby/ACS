from sqlmodel import select, func
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import UserLogModel, SystemLogModel
from app.schemas.chart import EmailLogChartRead
from app.schemas.log import (
    UserLogRead,
    UserLogUpdate,
    UserLogCreate,
    SystemLogRead,
    SystemLogUpdate,
    SystemLogCreate,
    AllUserLogRead,
)


class CRUDUserLog(
    CRUDBase[
        UserLogModel,
        UserLogCreate,
        UserLogUpdate,
        UserLogRead | AllUserLogRead,
    ]
):
    def get_select(self) -> Select | SelectOfScalar:
        return select(self.model).options(joinedload(self.model.user))


class CRUDSystemLog(
    CRUDBase[
        SystemLogModel,
        SystemLogCreate,
        SystemLogUpdate,
        SystemLogRead,
    ]
):
    async def chart(self) -> list[EmailLogChartRead]:
        response = await self.db.session.execute(
            select(
                self.model.event,
                func.count(self.model.event),
            )
            .group_by(self.model.event)
        )
        result = [
            EmailLogChartRead(event=event, count=count)
            for event, count in response.all()
        ]
        return result


crud_user_log = CRUDUserLog(model=UserLogModel)
crud_system_log = CRUDSystemLog(model=SystemLogModel)
