from pydantic import Field

from app.models import ApiBase, ApiGroupBase
from app.schemas.base import BaseCreatedAtRead, BaseUUIDRead
from app.utils.enums import ApiMethod
from app.utils.partial import optional


class ApiGroupRead(ApiGroupBase, BaseCreatedAtRead, BaseUUIDRead):
    ...


class ApiGroupDetailRead(ApiGroupBase, BaseCreatedAtRead, BaseUUIDRead):
    api_list: list['ApiRead'] = Field(
        description='Api列表',
        title='Api列表',
    )


class ApiGroupCreate(ApiGroupBase):
    ...


@optional
class ApiGroupUpdate(ApiGroupBase):
    ...


class ApiRead(ApiBase, BaseCreatedAtRead, BaseUUIDRead):
    uri: str = Field(
        title='Api',
        description='Api',
    )
    method: ApiMethod = Field(
        title='Api method',
        description='Api method',
    )
    description: str = Field(
        title='描述',
        description='描述',
    )


class ApiCreate(ApiBase):
    ...


@optional
class ApiUpdate(ApiBase):
    description: str = Field(
        title='描述',
        description='描述',
    )


ApiGroupDetailRead.update_forward_refs(ApiRead=ApiRead)
