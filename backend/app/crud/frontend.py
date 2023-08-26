from typing import Optional
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import FrontendModel
from app.schemas.frontend import (
    FrontendCreate,
    FrontendUpdate,
    FrontendRead,
)
from app.utils.sql_query import QueryList


class CRUDFrontend(
    CRUDBase[
        FrontendModel,
        FrontendCreate,
        FrontendUpdate,
        FrontendRead,
    ],
):
    def get_select(self):
        return select(self.model).options(selectinload(self.model.children))

    async def get_multi(
            self,
            query: Optional[QueryList] = None,
            db_session: Optional[AsyncSession] = None,
            paginated: bool = False,
    ) -> list[FrontendRead | FrontendModel]:
        db_session = db_session or self.db.session
        response = await db_session.execute(self.get_select().where(self.model.depth == 1))
        r = response.scalars().all()
        print(r)
        return r


crud_frontend = CRUDFrontend(model=FrontendModel)
