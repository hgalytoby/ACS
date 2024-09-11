from .api import ApiRead
from .frontend import FrontendRead
from .role import (
    RoleApiRead,
    RoleDetailRead,
    RoleFrontendListRead,
    RoleFrontendRead,
)
from .user import UserDetailRead

ApiRead.model_rebuild()
RoleApiRead.model_rebuild()
RoleDetailRead.model_rebuild()
RoleFrontendListRead.model_rebuild()
UserDetailRead.model_rebuild()
