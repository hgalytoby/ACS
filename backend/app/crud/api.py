from typing import Optional

from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.crud.base import CRUDBase
from app.models import ApiModel, ApiGroupModel
from app.schemas.api import (
    ApiCreate,
    ApiUpdate,
    ApiRead,
    ApiGroupCreate,
    ApiGroupUpdate,
    ApiGroupRead,
    ApiGroupDetailRead,
)


class CRUDApiGroup(
    CRUDBase[
        ApiGroupModel,
        ApiGroupCreate,
        ApiGroupUpdate,
        ApiGroupRead,
    ]
):
    async def update_api_ids(
            self,
            *,
            current_item: ApiGroupModel,
            api_items: list[ApiModel],
            db_session: Optional[AsyncSession] = None,
    ) -> ApiGroupDetailRead:
        db_session = db_session or self.db.session
        current_item.api_list = api_items
        instance = await self.save(instance=current_item, db_session=db_session)
        return ApiGroupDetailRead.from_orm(instance)


class CRUDApi(
    CRUDBase[
        ApiModel,
        ApiCreate,
        ApiUpdate,
        ApiRead,
    ]
):
    def get_select(self) -> Select | SelectOfScalar:
        return select(self.model).options(
            joinedload(self.model.group),
        )


crud_api_group = CRUDApiGroup(model=ApiGroupModel)
crud_api = CRUDApi(model=ApiModel)
