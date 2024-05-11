from arq.connections import RedisSettings
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import email_config, settings
from app.crud import crud_email_settings, crud_system_log, crud_user_log
from app.db.session import async_session_maker
from app.models import UserModel
from app.schemas.email import EmailSendCreate
from app.schemas.log import SystemLogCreate, UserLogCreate
from app.utils.enums import SystemLogEvent, UserLogEvent


async def send_email(subject: str, body: str, email: str):
    message = MessageSchema(
        subject=subject,
        recipients=[EmailStr(email)],
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(email_config)
    await fm.send_message(message=message)


async def send_register_email(ctx: dict, email: str, token: str):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_REGISTER,
            db_session=session,
        )
        body = instance.body.format(
            url=f'{settings.domain}/auth/verify?token={token}',
        )
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=email,
            body=body,
            event=SystemLogEvent.USER_REGISTER,
        )


async def send_verify_successfully_email(ctx: dict, user: UserModel):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_VERIFY,
            db_session=session,
        )
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=user.email,
            body=instance.body,
            event=SystemLogEvent.USER_VERIFY,
        )
        user_log = UserLogCreate(
            user_id=user.id,
            event=UserLogEvent.VERIFY_USER,
        )
        await crud_user_log.create(create_item=user_log, db_session=session)


async def send_forgot_password_email(ctx: dict, email: str, token: str):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_FORGOT_PASSWORD,
            db_session=session,
        )
        body = instance.body.format(
            url=f'{settings.domain}/auth/reset-password?token={token}'
        )
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=email,
            body=body,
            event=SystemLogEvent.USER_FORGOT_PASSWORD,
        )


async def send_reset_password_email(ctx: dict, email: str):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_RESET_PASSWORD,
            db_session=session,
        )
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=email,
            body=instance.body,
            event=SystemLogEvent.USER_RESET_PASSWORD,
        )


async def send_delete_email(
    ctx: dict,
    user: UserModel,
    current_user: UserModel,
):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_DESTROY,
            db_session=session,
        )
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=user.email,
            body=instance.body,
            event=SystemLogEvent.USER_DESTROY,
        )
        user_log = UserLogCreate(
            user_id=current_user.id,
            event=UserLogEvent.DESTROY_USER,
            raw_data={'email': user.email, 'user_id': str(user.id)},
        )
        await crud_user_log.create(create_item=user_log, db_session=session)


async def send_login_fail_email(ctx: dict, user: UserModel, ip: str):
    async with async_session_maker() as session:
        instance = await crud_email_settings.get_event(
            event=SystemLogEvent.USER_LOGIN_FAIL,
            db_session=session,
        )
        body = instance.body.format(ip=ip)
        await send_email_with_log(
            session=session,
            subject=instance.subject,
            email=user.email,
            body=body,
            event=SystemLogEvent.USER_LOGIN_FAIL,
        )


async def send_try_email(ctx: dict, subject: str, body: str, user: UserModel):
    async with async_session_maker() as session:
        await send_email(
            subject=subject, body=body, email='hgalytoby@gmail.com'
        )
        log = SystemLogCreate(
            raw_data={
                'user_id': str(user.id),
                'body': body,
                'subject': subject,
            },
            event=SystemLogEvent.TRY_SEND_EMAIL,
        )
        await crud_system_log.create(create_item=log, db_session=session)


async def send_email_with_log(
    session: AsyncSession,
    subject: str,
    email: str,
    body: str,
    event: SystemLogEvent,
):
    email_data = EmailSendCreate(subject=subject, email=email, body=body)
    raw_data = email_data.dict()
    await send_email(**raw_data)
    log = SystemLogCreate(raw_data=raw_data, event=event)
    await crud_system_log.create(create_item=log, db_session=session)


async def startup(ctx):
    ...


async def shutdown(ctx):
    ...


functions = [
    send_email,
    send_register_email,
    send_verify_successfully_email,
    send_forgot_password_email,
    send_reset_password_email,
    send_delete_email,
    send_login_fail_email,
    send_try_email,
]


class WorkerSettings:
    redis_settings = RedisSettings(host=settings.redis.host)
    functions = functions
    on_startup = startup
    on_shutdown = shutdown
