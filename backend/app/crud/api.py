from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.crud.base import CRUDBase
from app.models import ApiModel, ApiGroupModel
from app.schemas.api import (
    ApiCreate,
    ApiUpdate,
    ApiRead,
    ApiGroupCreate,
    ApiGroupUpdate,
    ApiGroupRead, ApiGroupDetailRead,
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
    ) -> ApiGroupDetailRead:
        current_item.api_ids = api_items
        self.db.session.add(current_item)
        await self.db.session.commit()
        await self.db.session.refresh(current_item)
        return ApiGroupDetailRead.from_orm(current_item)


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
