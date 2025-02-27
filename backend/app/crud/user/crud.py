from typing import Optional
from uuid import UUID

from fastapi import (
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.crud.base import CRUDBase
from app.crud.log import crud_user_log
from app.models import OAuthAccountModel, RoleModel, UserModel
from app.schemas.log import UserLogCreate
from app.schemas.user import (
    UserCreate,
    UserDetailRead,
    UserPasswordUpdate,
    UserRead,
    UserUpdate,
)
from app.utils.enums import UserLogEvent
from app.utils.storage import Storage


class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate, UserRead]):
    async def get(
        self,
        *,
        item_id: UUID,
        db_session: Optional[AsyncSession] = None,
    ) -> Optional[UserModel]:
        db_session = db_session or self.db.session
        query = self.get_select().where(self.model.id == item_id)
        response = await db_session.execute(query)
        return response.unique().scalar_one_or_none()

    async def update_user_to_roles(
        self,
        user: UserModel,
        role_list: list[RoleModel],
        db_session: Optional[AsyncSession] = None,
    ) -> UserDetailRead:
        db_session = db_session or self.db.session
        user.role_list = role_list
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
        user_log = UserLogCreate(
            user_id=user.id,
            event=UserLogEvent.UPDATE_USER,
            raw_data={'msg': 'update password'},
        )
        await crud_user_log.create(
            create_item=user_log,
            db_session=db_session,
            commit=False,
        )
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
        await Storage.save_image(instance=user, image=avatar)
        user = await self.update(
            current_item=user,
            update_item=update_item.dict(exclude_none=True),
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
                    select(OAuthAccountModel).where(
                        OAuthAccountModel.id == oauth.id,
                    ),
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
