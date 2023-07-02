from .role import RoleDetailRead, RoleApiRead
from .user import UserDetailRead
from .api import ApiRead

UserDetailRead.update_forward_refs(RoleApiRead=RoleApiRead)
RoleDetailRead.update_forward_refs(ApiRead=ApiRead)
RoleApiRead.update_forward_refs(ApiRead=ApiRead)
