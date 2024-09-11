from app.models import AcceptApiBase
from app.utils.partial import optional


class AcceptApiRead(AcceptApiBase):
    ...


class AcceptApiCreate(AcceptApiBase):
    ...


@optional()
class AcceptApiUpdate(AcceptApiBase):
    ...
