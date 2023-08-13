from datetime import datetime
from typing import Optional, Any
from uuid import UUID
import orjson
from fastapi import (
    Depends,
    Request,
    HTTPException,
    status,
    UploadFile,
    File,
    Response,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_async_sqlalchemy import db
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.jwt import decode_jwt, generate_jwt
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud.base import CRUDBase
from app.crud.log import crud_user_log
from app.models import UserModel, RoleModel, OAuthAccountModel
from app.schemas.log import UserLogCreate
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserPasswordUpdate,
    UserDetailRead,
)
from app.utils.enums import UserLogEvent
from app.utils.storage import Storage

SECRET = 'SECRET'


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
        user_id = decode_jwt(token, SECRET, ['fastapi-users:auth'], ['HS256'])['sub']
        return await self.user_db.get(id=user_id)

    async def delete(
            self,
            user: UserModel,
            request: Optional[Request] = None,
    ) -> None:
        await super().delete(user=user, request=self.request)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> Optional[UserModel]:
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None
        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            await self.on_after_login_fail(user=user)
            return None
        if updated_password_hash is not None:
            await self.user_db.update(user, {'hashed_password': updated_password_hash})
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
            user = await self.get_by_oauth_account(oauth_name, account_id)
        except exceptions.UserNotExists:
            try:
                user = await self.get_by_email(account_email)
                if not associate_by_email:
                    raise exceptions.UserAlreadyExists()
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)
            except exceptions.UserNotExists:
                password = self.password_helper.generate()
                user_dict = {
                    'email': account_email,
                    'hashed_password': self.password_helper.hash(password),
                    'is_verified': is_verified_by_default,
                    'username': account_email.split('@')[0],
                }
                user = await self.user_db.create(user_dict)
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)
                await self.on_after_oauth_register(user=user, request=request)
        else:
            user = await crud_user.get(item_id=user.id)
            for existing_oauth_account in user.oauth_accounts:
                if (
                        existing_oauth_account.account_id == account_id
                        and existing_oauth_account.oauth_name == oauth_name
                ):
                    user = await self.user_db.update_oauth_account(
                        user,
                        existing_oauth_account,
                        oauth_account_dict,
                    )

        return user

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        token = generate_jwt(
            data={
                'sub': str(user.id),
                'email': user.email,
                'aud': self.verification_token_audience,
            },
            secret=self.verification_token_secret,
            lifetime_seconds=self.verification_token_lifetime_seconds,
        )
        await request.state.arq.enqueue_job('send_register_email', user.email, token)

    async def on_after_oauth_register(self, user: UserModel, request: Optional[Request] = None):
        ...

    async def on_after_forgot_password(
            self,
            user: UserModel,
            token: str,
            request: Optional[Request] = None,
    ):
        print(f'User {user.id} has forgot their password. Reset token: {token}')
        await request.state.arq.enqueue_job('send_forgot_password_email', user.email, token)

    async def on_after_request_verify(
            self,
            user: UserModel,
            token: str,
            request: Optional[Request] = None,
    ):
        print(f'Verification requested for user {user.id}. Verification token: {token}')
        await request.state.arq.enqueue_job('send_register_email', user.email, token)

    async def on_after_update(
            self,
            user: UserModel,
            update_dict: dict[str, Any],
            request: Optional[Request] = None,
    ):
        if update_dict.get('password'):
            update_dict['password'] = '*' * len(update_dict['password'])
        print(f"User {user.id} has been updated with {update_dict}.")
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
        user.last_login = datetime.utcnow()
        await crud_user.save(instance=user)
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

    async def on_after_verify(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} has been verified")
        await request.state.arq.enqueue_job('send_verify_successfully_email', user)

    async def on_after_reset_password(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} has reset their password.")
        await request.state.arq.enqueue_job('send_reset_password_email', user.email)

    async def on_before_delete(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} is going to be deleted")

    async def on_after_delete(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} is successfully deleted")
        current_user = await self.get_current_user()
        await request.state.arq.enqueue_job('send_delete_email', user, current_user)


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


bearer_transport = BearerTransport(tokenUrl='api/v1/auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=60 * 60 * 24)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[UserModel, UUID](get_user_manager, [auth_backend])

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate, UserRead]):
    async def update_user_to_roles(
            self,
            user: UserModel,
            role_list: list[RoleModel],
            db_session: Optional[AsyncSession] = None,
    ) -> UserDetailRead:
        db_session = db_session or self.db.session
        user.role_ids = role_list
        instance = await self.save(instance=user, db_session=db_session)
        return UserDetailRead.from_orm(instance)

    async def update_password(
            self,
            user: UserModel,
            password: UserPasswordUpdate,
            db_session: Optional[AsyncSession] = None,
    ) -> UserRead:
        db_session = db_session or self.db.session
        password_helper = PasswordHelper()
        verified, _ = password_helper.verify_and_update(
            plain_password=password.old_password,
            hashed_password=user.hashed_password,
        )
        if not verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        new_password = password_helper.hash(password=password.new_password)
        await self.update(
            current_item=user,
            update_item={'hashed_password': new_password},
            db_session=db_session,
        )
        return UserRead.from_orm(user)

    async def update_info(
            self,
            user: UserModel,
            update_item: UserUpdate,
            avatar: UploadFile = File(None),
            db_session: Optional[AsyncSession] = None,
    ) -> UserRead:
        db_session = db_session or self.db.session
        await Storage.save_image(instance=user, image=avatar)
        user = await self.update(
            current_item=user,
            update_item=update_item,
            db_session=db_session,
        )
        return UserRead.from_orm(user)

    async def get_first_created_at_user(
            self,
            *,
            db_session: Optional[AsyncSession] = None,
    ) -> UserModel:
        db_session = db_session or self.db.session
        expression = self.get_select().order_by(self.model.created_at.asc())
        response = await db_session.execute(expression)
        return response.scalars().first()

    async def unlink_oauth(
            self,
            provider_name: str,
            user: UserModel,
            db_session: Optional[AsyncSession] = None,
    ) -> UserRead:
        for oauth in user.oauth_accounts:
            if oauth.oauth_name == provider_name:
                db_session = db_session or self.db.session
                response = await db_session.execute(
                    select(OAuthAccountModel)
                    .where(OAuthAccountModel.id == oauth.id)
                )
                oauth_obj = response.scalar_one()
                await db_session.delete(oauth_obj)
                user.oauth_accounts.remove(oauth)
                await self.save(
                    instance=user,
                    db_session=db_session,
                )
                return UserRead.from_orm(user)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='UnLink.',
        )



crud_user = CRUDUser(model=UserModel)