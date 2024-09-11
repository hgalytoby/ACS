from typing import Any, Optional
from uuid import UUID

from fastapi import (
    Depends,
    Request,
    Response,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_async_sqlalchemy import db
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    RedisStrategy,
)
from fastapi_users.jwt import decode_jwt, generate_jwt
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
import orjson

from app.core.config import settings
from app.crud.log import crud_user_log
from app.models import OAuthAccountModel, UserModel
from app.schemas.log import UserLogCreate
from app.schemas.user import UserUpdate
from app.utils.enums import UserLogEvent
from app.utils.redis import init_redis_pool

SECRET = 'SECRET'
TOKEN_AUDIENCE = ['fastapi-users:auth']


class MySQLModelUserDatabaseAsync(SQLModelUserDatabaseAsync[UserModel, UUID]):
    async def delete(self, user: UserModel) -> None:
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)


class UserManager(UUIDIDMixin, BaseUserManager[UserModel, UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __init__(
        self,
        user_db: MySQLModelUserDatabaseAsync,
        request: Request,
    ):
        super(UserManager, self).__init__(user_db)
        self.request = request

    async def get_current_user(self) -> UserModel:
        """
        取得當前登入的使用者。
        :return:
        """
        token = self.request.headers['authorization'].split()[1]
        user_id = decode_jwt(
            encoded_jwt=token,
            secret=SECRET,
            audience=TOKEN_AUDIENCE,
            algorithms=['HS256'],
        )['sub']
        return await self.user_db.get(id=user_id)

    async def update(
        self,
        user_update: dict,
        user: UserModel,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> UserModel:
        user_update = UserUpdate(**user_update)
        if safe:
            updated_user_data = user_update.create_update_dict()
        else:
            updated_user_data = user_update.create_update_dict_superuser()

        updated_user = await self._update(
            user=user,
            update_dict=updated_user_data,
        )
        await self.on_after_update(
            user=updated_user,
            update_dict=updated_user_data,
            request=request,
        )
        return updated_user

    async def delete(
        self,
        user: UserModel,
        request: Optional[Request] = None,
    ) -> None:
        await super().delete(user=user, request=self.request)

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[UserModel]:
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        (
            verified,
            updated_password_hash,
        ) = self.password_helper.verify_and_update(
            plain_password=credentials.password,
            hashed_password=user.hashed_password,
        )

        if not verified:
            await self.on_after_login_fail(user=user)
            return None

        if updated_password_hash is not None:
            await self.user_db.update(
                user=user,
                update_dict={'hashed_password': updated_password_hash},
            )

        return user

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> UserModel:
        oauth_account_dict = {
            'oauth_name': oauth_name,
            'access_token': access_token,
            'account_id': account_id,
            'account_email': account_email,
            'expires_at': expires_at,
            'refresh_token': refresh_token,
        }

        try:
            user = await self.get_by_oauth_account(
                oauth=oauth_name,
                account_id=account_id,
            )
        except exceptions.UserNotExists:
            try:
                user = await self.get_by_email(account_email)
                if not associate_by_email:
                    raise exceptions.UserAlreadyExists()
                user = await self.user_db.add_oauth_account(
                    user, oauth_account_dict
                )
            except exceptions.UserNotExists:
                password = self.password_helper.generate()
                user_dict = {
                    'email': account_email,
                    'hashed_password': self.password_helper.hash(password),
                    'is_verified': is_verified_by_default,
                    'username': account_email.split('@')[0],
                }
                user = await self.user_db.create(user_dict)
                user = await self.user_db.add_oauth_account(
                    user=user,
                    create_dict=oauth_account_dict,
                )
                await self.on_after_oauth_register(user=user, request=request)
        else:
            # user = await crud_user.get(item_id=user.id)
            for existing_oauth_account in user.oauth_accounts:
                if (
                    existing_oauth_account.account_id == account_id
                    and existing_oauth_account.oauth_name == oauth_name
                ):
                    user = await self.user_db.update_oauth_account(
                        user=user,
                        oauth_account=existing_oauth_account,
                        update_dict=oauth_account_dict,
                    )

        return user

    async def on_after_register(
        self, user: UserModel, request: Optional[Request] = None
    ):
        token = generate_jwt(
            data={
                'sub': str(user.id),
                'email': user.email,
                'aud': self.verification_token_audience,
            },
            secret=self.verification_token_secret,
            lifetime_seconds=self.verification_token_lifetime_seconds,
        )
        await request.state.arq.enqueue_job(
            'send_register_email', user.email, token
        )

    async def on_after_oauth_register(
        self, user: UserModel, request: Optional[Request] = None
    ):
        ...

    async def on_after_forgot_password(
        self,
        user: UserModel,
        token: str,
        request: Optional[Request] = None,
    ):
        print(f'User {user.id} has forgot their password. Reset token: {token}')
        await request.state.arq.enqueue_job(
            'send_forgot_password_email', user.email, token
        )

    async def on_after_request_verify(
        self,
        user: UserModel,
        token: str,
        request: Optional[Request] = None,
    ):
        print(
            f'Verification requested for user {user.id}. Verification token: {token}'
        )
        await request.state.arq.enqueue_job(
            'send_register_email', user.email, token
        )

    async def on_after_update(
        self,
        user: UserModel,
        update_dict: dict[str, Any],
        request: Optional[Request] = None,
    ):
        if update_dict.get('password'):
            update_dict['password'] = '*' * len(update_dict['password'])

        print(f'User {user.id} has been updated with {update_dict}.')
        user_log = UserLogCreate(
            user_id=user.id,
            event=UserLogEvent.UPDATE_USER,
            raw_data=update_dict,
        )
        await crud_user_log.create(create_item=user_log)

    async def on_after_login(
        self,
        user: UserModel,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        user_log = UserLogCreate(
            user_id=user.id,
            event=UserLogEvent.LOGIN_USER,
            raw_data={'host': self.request.client.host},
        )
        await crud_user_log.create(create_item=user_log)

    async def on_after_login_fail(self, user: UserModel):
        redis = self.request.state.redis
        cache = await redis.get(user.email)
        if not cache:
            await redis.set(
                user.email,
                orjson.dumps({'count': 1, 'n': 1}),
            )
        else:
            cache = orjson.loads(cache)
            if cache['count'] > cache['n'] * 5:
                await self.request.state.arq.enqueue_job(
                    'send_login_fail_email',
                    user,
                    self.request.client.host,
                )
                cache['n'] += 1
                cache['count'] = 0
            else:
                cache['count'] += 1
            await redis.set(user.email, orjson.dumps(cache))

    async def on_after_verify(
        self, user: UserModel, request: Optional[Request] = None
    ):
        print(f'User {user.id} has been verified')
        await request.state.arq.enqueue_job(
            'send_verify_successfully_email', user
        )

    async def on_after_reset_password(
        self, user: UserModel, request: Optional[Request] = None
    ):
        print(f'User {user.id} has reset their password.')
        await request.state.arq.enqueue_job(
            'send_reset_password_email', user.email
        )

    async def on_before_delete(
        self, user: UserModel, request: Optional[Request] = None
    ):
        print(f'User {user.id} is going to be deleted')

    async def on_after_delete(
        self, user: UserModel, request: Optional[Request] = None
    ):
        print(f'User {user.id} is successfully deleted')
        current_user = await self.get_current_user()
        await request.state.arq.enqueue_job(
            'send_delete_email', user, current_user
        )


async def get_user_db():
    yield MySQLModelUserDatabaseAsync(db.session, UserModel, OAuthAccountModel)


async def get_user_manager(
    request: Request,
    user_db: MySQLModelUserDatabaseAsync = Depends(get_user_db),
):
    yield UserManager(
        user_db=user_db,
        request=request,
    )


bearer_transport = BearerTransport(tokenUrl='api/v1/auth/login')


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(
        redis=init_redis_pool(),
        lifetime_seconds=3600,
        key_prefix=settings.token_key_prefix,
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[UserModel, UUID](get_user_manager, [auth_backend])

current_active_verified_user = fastapi_users.current_user(
    active=True,
    verified=True,
)
