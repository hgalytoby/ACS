from enum import Enum
from functools import cache


class AppEnv(Enum):
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    TESTING = 'test'


class AllowedImageExtensions(str, Enum):
    JPEG = 'jpeg'
    JPG = 'jpg'
    PNG = 'png'
    WEBP = 'webp'
    GIF = 'gif'
    ICO = 'ico'

    @classmethod
    @cache
    def rule(cls):
        return {member.value for member in AllowedImageExtensions}

    @classmethod
    def valid(cls, type_: str):
        return type_ in cls.rule()


class ImageFailDetail(str, Enum):
    INVALID_IMAGE_FORMAT = 'INVALID_IMAGE_FORMAT'


class UserFailDetail(str, Enum):
    USER_EMAIL_EXIST = 'USER_EMAIL_EXIST'


class SteinsGate(str, Enum):
    PLAN = 'Operation Skuld, El Psy Congroo.'
    DIVERGENCE = '1.048596'


class WebSocketEvent(str, Enum):
    MEMBER_STATUS = 'MEMBER_STATUS'
    MEMBER_STATUS_LIST = 'MEMBER_STATUS_LIST'
    LOGIN = 'LOGIN'
    CHANNEL = 'ACS'


class BaseEventEnum(Enum):
    def __new__(cls, value, doc=None):
        self = object.__new__(cls)
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self

    @classmethod
    def md(cls):
        result = '''
        '''
        result += '''
        '''.join([f'{item.name} = {item.__doc__}' for item in cls])
        return result


class BaseEvent(Enum):
    USER_REGISTER = 'UserRegister', '使用者註冊'
    USER_LOGIN_FAIL = 'UserLoginFail', '使用者登入失敗'
    USER_FORGOT_PASSWORD = 'UserForgotPassword', '使用者忘記密碼'
    USER_RESET_PASSWORD = 'UserResetPassword', '使用者重置密碼'
    USER_VERIFY = 'UserVerify', '啟用使用者'
    USER_DESTROY = 'UserDestroy', '刪除使用者'


class UserLogEvent(BaseEventEnum):
    CREATE_MEMBER = 'CreateMember', '新增成員'
    UPDATE_MEMBER = 'UpdateMember', '更新成員'
    DESTROY_MEMBER = 'DestroyMember', '刪除成員'
    CREATE_MEMBER_LOCATION = 'CreateMemberLocation', '新增地點'
    UPDATE_MEMBER_LOCATION = 'UpdateMemberLocation', '更新地點'
    DESTROY_MEMBER_LOCATION = 'DestroyMemberLocation', '刪除地點'
    LOGIN_USER = 'LoginUser', '使用者登入'
    VERIFY_USER = 'VerifyUser', '啟用使用者'
    UPDATE_USER = 'UpdateUser', '更新使用者'
    DESTROY_USER = 'DestroyUser', '刪除使用者'


# 無法繼承拓展。
class SystemLogEvent(BaseEventEnum):
    USER_REGISTER = 'UserRegister', '使用者註冊'
    USER_LOGIN_FAIL = 'UserLoginFail', '使用者登入失敗'
    USER_FORGOT_PASSWORD = 'UserForgotPassword', '使用者忘記密碼'
    USER_RESET_PASSWORD = 'UserResetPassword', '使用者重置密碼'
    USER_VERIFY = 'UserVerify', '啟用使用者'
    USER_DESTROY = 'UserDestroy', '刪除使用者'
    TRY_SEND_EMAIL = 'TrySendEmail', '測試送信'


class EmailEventDefaultValue(str, Enum):
    REGISTER_SUBJECT = '{project} 啟用帳號信'
    REGISTER_BODY = '{project} 啟用帳號信 網址: {url}'
    FORGOT_PASSWORD_SUBJECT = '{project} 忘記密碼信'
    FORGOT_PASSWORD_BODY = '{project} 忘記密碼信 網址: {url}'
    RESET_PASSWORD_SUBJECT = '{project} 已更改密碼'
    RESET_PASSWORD_BODY = '已更改密碼'
    VERIFY_SUBJECT = '歡迎使用 {project}'
    VERIFY_BODY = '歡迎使用 {project}'
    DELETE_SUBJECT = '{project} 刪除使用者'
    DELETE_BODY = '您的帳號已被刪除!'
    LOGIN_FAIL_SUBJECT = '{project} 登入失敗'
    LOGIN_FAIL_BODY = '您的帳號從 IP: {ip} 於 10 分鐘內多次登入失敗!'


class ApiMethod(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class BloodType(str, Enum):
    A = 'A'
    B = 'B'
    AB = 'AB'
    O = 'O'


class StorageType(str, Enum):
    LOCAL = 'LOCAL'
    GCP = 'GCP'


class APIAccess(str, Enum):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
