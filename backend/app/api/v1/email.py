from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_restful.cbv import cbv

from app.crud import crud_email_settings
from app.crud.user import current_active_verified_user
from app.models import UserModel
from app.schemas.email import (
    EmailSettingsRead,
    EmailSettingsUpdate,
    EmailTrySendSchema,
)
from app.utils.enums import APIAccess, SystemLogEvent

router = APIRouter(tags=['信箱設定'])


@cbv(router)
class EmailView:
    user: UserModel = Depends(current_active_verified_user)

    @router.get(
        '/email-settings',
        name=APIAccess.PRIVATE,
        summary='取得信箱設定',
        status_code=status.HTTP_200_OK,
        tags=['信箱設定'],
    )
    async def get_multi(self) -> list[EmailSettingsRead]:
        return await crud_email_settings.get_multi()

    @router.get(
        '/email-settings/{event}',
        name=APIAccess.PRIVATE,
        summary='信箱設定',
        status_code=status.HTTP_200_OK,
    )
    async def get(self, event: SystemLogEvent) -> EmailSettingsRead:
        instance = await crud_email_settings.get_event(event=event)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return EmailSettingsRead.from_orm(instance)

    @router.patch(
        '/email-settings/{event}',
        name=APIAccess.PRIVATE,
        summary='信箱設定',
        status_code=status.HTTP_200_OK,
    )
    async def update(
        self,
        event: SystemLogEvent,
        item: EmailSettingsUpdate,
    ) -> EmailSettingsRead:
        instance = await crud_email_settings.get_event(event=event)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        instance = await crud_email_settings.update(
            current_item=instance,
            update_item=item,
        )
        return EmailSettingsRead.from_orm(instance)

    @router.post(
        '/email-try-send',
        name=APIAccess.PRIVATE,
        summary='測試送信',
        status_code=status.HTTP_202_ACCEPTED,
    )
    async def post(self, request: Request, email_try_send: EmailTrySendSchema):
        body = email_try_send.get_sample_body(request=request)
        await request.state.arq.enqueue_job(
            'send_try_email',
            email_try_send.subject,
            body,
            self.user,
        )
