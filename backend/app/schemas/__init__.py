from .role import RoleFrontendRead, RoleApiRead, RoleDetailRead
from .user import UserDetailRead
from .api import ApiRead
from .frontend import FrontendRead

UserDetailRead.update_forward_refs(RoleFrontendRead=RoleFrontendRead)
RoleFrontendRead.update_forward_refs(FrontendRead=FrontendRead)
RoleApiRead.update_forward_refs(ApiRead=ApiRead)
RoleDetailRead.update_forward_refs(ApiRead=ApiRead)
