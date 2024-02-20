from collections import defaultdict
from uuid import uuid4

from fastapi.routing import APIRoute
from fastapi_users.password import PasswordHelper
from sqlmodel.ext.asyncio.session import AsyncSession

from app import crud
from app.core.config import settings
from app.crud.user import MySQLModelUserDatabaseAsync
from app.main import app
from app.models import (
    ApiGroupModel,
    ApiModel,
    EmailSettingsModel,
    OAuthAccountModel,
    RoleModel,
    UserModel,
)
from app.schemas.accept import AcceptApiCreate
from app.utils.enums import APIAccess, ApiMethod, SystemLogEvent
from app.utils.sql_query import QueryList


async def create_superuser(db_session: AsyncSession):
    root = 'root@example.com'
    user_db = MySQLModelUserDatabaseAsync(
        session=db_session,
        user_model=UserModel,
        oauth_account_model=OAuthAccountModel,
    )

    if await user_db.get_by_email(email=root):
        return

    password_helper = PasswordHelper()
    password = password_helper.hash('00000000')

    user = UserModel(
        id=uuid4(),
        email=root,
        is_active=True,
        is_superuser=True,
        is_verified=True,
        username='root',
        hashed_password=password,
        avatar='',
    )
    await user_db.create(create_dict=user.dict())


async def create_accept_api(db_session: AsyncSession):
    if await crud.crud_accept_api.get_first(db_session=db_session):
        return

    create_item = AcceptApiCreate(api='/api/v1/member-come')
    await crud.crud_accept_api.create(
        create_item=create_item,
        db_session=db_session
    )


async def create_email_register(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_REGISTER,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_REGISTER,
            subject=f'{settings.project} 啟用帳號信',
            body=settings.project + ' 啟用帳號信 網址: {url}',
        ),
        db_session=db_session
    )


async def create_email_forgot_password(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_FORGOT_PASSWORD,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_FORGOT_PASSWORD,
            subject=f'{settings.project} 忘記密碼信',
            body=settings.project + ' 忘記密碼信 網址: {url}',
        ),
        db_session=db_session
    )


async def create_email_reset_password(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_RESET_PASSWORD,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_RESET_PASSWORD,
            subject=f'{settings.project} 已更改密碼',
            body='已更改密碼',
        ),
        db_session=db_session
    )


async def create_email_verify(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_VERIFY,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_VERIFY,
            subject=f'歡迎使用 {settings.project}',
            body=f'歡迎使用 {settings.project}!',
        ),
        db_session=db_session
    )


async def create_email_delete(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_DESTROY,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_DESTROY,
            subject=f'{settings.project} 刪除使用者',
            body='您的帳號已被刪除!',
        ),
        db_session=db_session
    )


async def create_email_login_fail(db_session: AsyncSession):
    if await crud.crud_email_settings.get_event(
        event=SystemLogEvent.USER_LOGIN_FAIL,
        db_session=db_session,
    ):
        return

    await crud.crud_email_settings.create(
        create_item=EmailSettingsModel(
            event=SystemLogEvent.USER_LOGIN_FAIL,
            subject=f'{settings.project} 登入失敗',
            body='您的帳號從 IP: {ip} 多次登入失敗!',
        ),
        db_session=db_session
    )


async def create_email_settings(db_session: AsyncSession):
    await create_email_register(db_session=db_session)
    await create_email_forgot_password(db_session=db_session)
    await create_email_reset_password(db_session=db_session)
    await create_email_verify(db_session=db_session)
    await create_email_delete(db_session=db_session)
    await create_email_login_fail(db_session=db_session)


def get_route() -> list[APIRoute]:
    private_exception_list = ('users',)
    for route in app.routes:
        if route.name == APIAccess.PRIVATE:
            yield route
            continue

        for private in private_exception_list:
            if route.name.startswith(private):
                yield route


async def create_api(db_session: AsyncSession):
    for route in get_route():
        query = QueryList(
            query=[
                crud.crud_api.model.uri == route.path,
                crud.crud_api.model.method == list(route.methods)[0],
            ]
        )

        if not await crud.crud_api.get_first(db_session=db_session, query=query):
            api_model = ApiModel(
                uri=str(route.path),
                method=ApiMethod[list(route.methods)[0]],
                description=route.summary or route.name,
            )
            await crud.crud_api.create(
                db_session=db_session,
                create_item=api_model,
            )


async def create_api_group(db_session: AsyncSession):
    tags = {}
    for route in get_route():
        tags[route.tags[0]] = ApiGroupModel(name=route.tags[0])

    query = QueryList(
        query=[
            crud.crud_api_group.model.name.in_(tags.keys()),
        ]
    )

    items = await crud.crud_api_group.get_multi(query=query, db_session=db_session)
    for item in items:
        tags.pop(item.name)

    db_session.add_all(tags.values())
    await db_session.commit()


async def add_api_to_api_group(db_session: AsyncSession):
    group = defaultdict(list)
    for route in get_route():
        query = QueryList(
            query=[
                crud.crud_api.model.uri == route.path,
                crud.crud_api.model.method == list(route.methods)[0],
            ]
        )
        api_item = await crud.crud_api.get_first(db_session=db_session, query=query)
        group[route.tags[0]].append(api_item)

    for group_name, api_list in group.items():
        query = QueryList(
            query=[
                crud.crud_api_group.model.name == group_name,
            ]
        )
        group_item = await crud.crud_api_group.get_first(query=query, db_session=db_session)

        for api in api_list:
            if not api.group:
                api.group = group_item
                db_session.add(api)

    await db_session.commit()


async def create_role(db_session: AsyncSession):
    role_init_items = {
        'Boss': RoleModel(name='Boss'),
        'Guest': RoleModel(name='Guest'),
    }
    roles = await crud.crud_role.get_multi(
        query=QueryList(
            query=[
                crud.crud_role.model.name.in_(role_init_items.keys())
            ]
        ),
        db_session=db_session,
    )
    for role in roles:
        role_init_items.pop(role.name)

    db_session.add_all(role_init_items.values())
    await db_session.commit()


async def init_db(db_session: AsyncSession):
    await create_superuser(db_session=db_session)
    await create_accept_api(db_session=db_session)
    await create_email_settings(db_session=db_session)
    await create_api(db_session=db_session)
    await create_api_group(db_session=db_session)
    await add_api_to_api_group(db_session=db_session)
    await create_role(db_session=db_session)
