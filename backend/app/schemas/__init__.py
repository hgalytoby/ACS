from .api import ApiRead
from .frontend import FrontendRead
from .role import RoleApiRead, RoleDetailRead, RoleFrontendListRead, RoleFrontendRead
from .user import UserDetailRead

UserDetailRead.update_forward_refs(RoleFrontendListRead=RoleFrontendListRead)
# RoleFrontendRead.update_forward_refs(FrontendRead=FrontendRead)
RoleApiRead.update_forward_refs(ApiRead=ApiRead)
RoleDetailRead.update_forward_refs(ApiRead=ApiRead)
