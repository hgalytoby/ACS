from app.crud.base import CRUDBase
from app.models import AcceptApiModel
from app.schemas.accept import AcceptApiCreate, AcceptApiRead, AcceptApiUpdate


class CRUDAcceptApi(
    CRUDBase[
        AcceptApiModel,
        AcceptApiCreate,
        AcceptApiUpdate,
        AcceptApiRead,
    ],
):
    ...


crud_accept_api = CRUDAcceptApi(model=AcceptApiModel)
