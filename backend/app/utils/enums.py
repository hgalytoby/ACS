from enum import Enum
from functools import cache


class MyEnum(Enum):
    @classmethod
    @cache
    def values(cls) -> list[str]:
        return [member.value for member in cls]


class AppEnvPath(str, MyEnum):
    """
    PROD = 正式環境
    DEV = 開發環境
    TEST = 測試環境
    """

    PROD = '.env'
    DEV = '.env.dev'
    TEST = '.env.test'


class AppEnv(str, MyEnum):
    """
    PROD = 正式環境
    DEV = 開發環境
    TEST = 測試環境
    """

    PROD = 'PROD'
    DEV = 'DEV'
    TEST = 'TEST'


class AllowedImageExtensions(str, MyEnum):
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


class ImageFailDetail(str, MyEnum):
    INVALID_IMAGE_FORMAT = 'INVALID_IMAGE_FORMAT'


class UserFailDetail(str, MyEnum):
    USER_EMAIL_EXIST = 'USER_EMAIL_EXIST'


class SteinsGate(str, MyEnum):
    PLAN = 'Operation Skuld, El Psy Congroo.'
    DIVERGENCE = '1.048596'


class WebSocketEvent(str, MyEnum):
    """
    MEMBER_STATUS = 成員狀態
    MEMBER_STATUS_LIST = 成原列表
    LOGIN = 登入
    CHANNEL = 頻道
    """

    MEMBER_STATUS = 'MEMBER_STATUS'
    MEMBER_STATUS_LIST = 'MEMBER_STATUS_LIST'
    LOGIN = 'LOGIN'
    CHANNEL = 'ACS'


class UserLogEvent(str, MyEnum):
    """
    CREATE_MEMBER = 新增成員
    UPDATE_MEMBER = 更新成員
    DESTROY_MEMBER = 刪除成員
    CREATE_MEMBER_LOCATION = 新增地點
    UPDATE_MEMBER_LOCATION = 更新地點
    DESTROY_MEMBER_LOCATION = 刪除地點
    LOGIN_USER = 使用者登入
    VERIFY_USER = 驗證使用者
    UPDATE_USER = 更新使用者
    DESTROY_USER = 刪除使用者
    """

    CREATE_MEMBER = 'CreateMember'
    UPDATE_MEMBER = 'UpdateMember'
    DESTROY_MEMBER = 'DestroyMember'
    CREATE_MEMBER_LOCATION = 'CreateMemberLocation'
    UPDATE_MEMBER_LOCATION = 'UpdateMemberLocation'
    DESTROY_MEMBER_LOCATION = 'DestroyMemberLocation'
    LOGIN_USER = 'LoginUser'
    VERIFY_USER = 'VerifyUser'
    UPDATE_USER = 'UpdateUser'
    DESTROY_USER = 'DestroyUser'


# 無法繼承拓展。
class SystemLogEvent(str, MyEnum):
    """
    USER_REGISTER = 使用者註冊
    USER_LOGIN_FAIL = 使用者登入失敗
    USER_FORGOT_PASSWORD = 使用者忘記密碼
    USER_RESET_PASSWORD = 使用者重置密碼
    USER_VERIFY = 驗證使用者
    USER_DESTROY = 刪除使用者
    TRY_SEND_EMAIL = 測試送信
    """

    USER_REGISTER = 'UserRegister'
    USER_LOGIN_FAIL = 'UserLoginFail'
    USER_FORGOT_PASSWORD = 'UserForgotPassword'
    USER_RESET_PASSWORD = 'UserResetPassword'
    USER_VERIFY = 'UserVerify'
    USER_DESTROY = 'UserDestroy'
    TRY_SEND_EMAIL = 'TrySendEmail'


class EmailEventDefaultValue(str, MyEnum):
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


class ApiMethod(str, MyEnum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class BloodType(str, MyEnum):
    A = 'A'
    B = 'B'
    AB = 'AB'
    O = 'O'


class StorageType(str, MyEnum):
    """
    LOCAL = 本地端
    GCP = Google Cloud Storage
    """

    LOCAL = 'LOCAL'
    GCP = 'GCP'


class APIAccess(str, MyEnum):
    """
    PUBLIC = 公
    PRIVATE = 私
    """

    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'


class HardDiskVolumeLabel(str, MyEnum):
    TOTAL = 'Total(GB)'
    USED = 'Used(GB)'
    FREE = 'Free(GB)'
