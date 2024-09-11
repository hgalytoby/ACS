from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models import FrontendModel
from app.schemas.frontend import (
    FrontendCreate,
    FrontendRead,
    FrontendUpdate,
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
        """"""
        db_session = db_session or self.db.session
        # 如果用以下這行，第二層以後會沒有 selectinload 導致拿不到第二層以後的資料。
        # 暫時沒解決方法只好自己篩選了。
        response = await db_session.execute(self.get_select())
        return [item for item in response.scalars().all() if item.depth == 1]


crud_frontend = CRUDFrontend(model=FrontendModel)
