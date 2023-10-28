from collections import defaultdict
from typing import Optional, Any
from uuid import UUID
from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy.orm import joinedload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.crud.base import CRUDBase
from app.models import (
    MemberLocationModel,
    MemberModel,
    MemberRecordModel,
    MemberStatusModel,
)
from app.schemas.chart import (
    BaseGrowthRead,
    MemberRecordHourlyCountRead,
    MemberRecordHourlyCountDataRead,
)
from app.schemas.member import (
    MemberLocationUpdate,
    MemberLocationRead,
    MemberLocationCreate,
    MemberCreate,
    MemberUpdate,
    MemberRead,
    MemberRecordCreate,
    MemberRecordUpdate,
    MemberRecordRead,
    MemberStatusCreate,
    MemberStatusUpdate,
    MemberStatusRead,
    MemberStatusCreatedRead,
)
from app.utils.chart import DateGrowthChart
from app.utils.sql_query import QueryList, DateRelatedQueryList
from app.utils.storage import Storage


class CRUDMemberLocation(
    CRUDBase[
        MemberLocationModel,
        MemberLocationCreate,
        MemberLocationUpdate,
        MemberLocationRead,
    ]
):
    async def create(
        self,
        *,
        create_item: MemberLocationCreate | MemberLocationModel,
        image: UploadFile = File(),
        db_session: Optional[AsyncSession] = None,
    ) -> MemberLocationModel:
        instance = await super().create(create_item=create_item, db_session=db_session)
        await Storage.save_image(instance=instance, image=image)
        instance = await self.save(instance=instance, db_session=db_session)
        return instance

    async def update(
        self,
        *,
        current_item: MemberLocationModel,
        update_item: MemberLocationUpdate | dict[str, Any] | MemberLocationModel,
        db_session: Optional[AsyncSession] = None,
        image: UploadFile = File(default=None),
    ) -> MemberLocationModel:
        instance = await super().update(
            current_item=current_item,
            update_item=update_item,
            db_session=db_session,
        )
        await Storage.save_image(instance=instance, image=image)
        instance = await self.save(instance=instance)
        return instance

    async def destroy(
        self,
        *,
        item_id: UUID | str,
        db_session: Optional[AsyncSession] = None,
    ) -> MemberLocationModel:
        member_exist = await crud_member_status.get_first(
            query=QueryList(
                query=[
                    MemberStatusModel.member_location_id == item_id,
                ],
            ),
        )

        if member_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Deletion not allowed. Members exist.',
            )

        instance = await super().destroy(item_id=item_id, db_session=db_session)
        return instance


class CRUDMember(
    CRUDBase[
        MemberModel,
        MemberCreate,
        MemberUpdate,
        MemberRead,
    ]
):
    async def create(
        self,
        *,
        create_item: MemberCreate | MemberModel,
        image: UploadFile = File(),
        db_session: Optional[AsyncSession] = None,
    ) -> MemberModel:
        instance = await super().create(
            create_item=create_item,
            db_session=db_session,
        )
        print(123)
        await Storage.save_image(instance=instance, image=image)
        await Storage.save_qrcode(instance=instance)
        instance = await self.save(instance=instance)
        return instance

    async def update(
        self,
        *,
        current_item: MemberModel,
        update_item: MemberUpdate | dict[str, Any] | MemberModel,
        db_session: Optional[AsyncSession] = None,
        image: UploadFile = File(default=None),
    ) -> MemberModel:
        instance = await super().update(
            current_item=current_item,
            update_item=update_item,
            db_session=db_session,
        )
        await Storage.save_image(instance=instance, image=image)
        instance = await self.save(instance=instance)
        return instance

    async def destroy(
        self,
        *,
        item_id: UUID | str,
        db_session: Optional[AsyncSession] = None,
    ) -> MemberModel:
        member_status_exist = await crud_member_status.get_first(
            query=QueryList(
                query=[
                    MemberStatusModel.member_id == item_id,
                ],
            ),
        )

        if member_status_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Deletion not allowed. '
                       f'The member is located within the {member_status_exist.member_location.name} '
                       f'and cannot be deleted.',
            )

        instance = await super().destroy(item_id=item_id, db_session=db_session)
        await Storage.remove_qr_code(instance=instance)
        await Storage.remove_image(instance=instance)
        return instance

    async def growth_chart(
        self,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await self.get_multi(query=query)
        result = DateGrowthChart.calculate_date_growth(
            start_date=query.date_range[0],
            end_date=query.date_range[1],
            accumulate=True,
            items=items,
        )
        return result

    async def new_member_growth_chart(
        self,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await self.get_multi(query=query)
        result = DateGrowthChart.calculate_date_growth(
            start_date=query.date_range[0],
            end_date=query.date_range[1],
            accumulate=False,
            items=items,
        )
        return result


class CRUDMemberRecord(
    CRUDBase[
        MemberRecordModel,
        MemberRecordCreate,
        MemberRecordUpdate,
        MemberRecordRead,
    ]
):
    async def member_record_growth_chart(
        self,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await self.get_multi(query=query)
        return DateGrowthChart.calculate_date_growth(
            start_date=query.date_range[0],
            end_date=query.date_range[1],
            items=items,
            accumulate=True,
        )

    async def member_record_hourly_count_chart(
        self,
        query: DateRelatedQueryList,
    ) -> MemberRecordHourlyCountRead:
        items = await self.get_multi(query=query)
        result = [MemberRecordHourlyCountDataRead(hour=i) for i in range(25)]

        for item in items:  # type: MemberRecordModel
            result[item.created_at.hour].count += 1

        return MemberRecordHourlyCountRead(
            data=result,
            start_date=query.date_range[0],
            end_date=query.date_range[1],
        )


class CRUDMemberStatus(
    CRUDBase[
        MemberStatusModel,
        MemberStatusCreate,
        MemberStatusUpdate,
        MemberStatusRead,
    ]
):
    def get_select(self) -> Select | SelectOfScalar:
        return select(self.model).options(
            joinedload(self.model.member_location),
            joinedload(self.model.member),
        )

    async def get(
        self,
        *,
        item_id: UUID,
        db_session: Optional[AsyncSession] = None,
    ) -> Optional[MemberStatusModel]:
        db_session = db_session or self.db.session
        query = self.get_select().where(self.model.member_id == item_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_multi(
        self,
        query: Optional[QueryList] = None,
        db_session: Optional[AsyncSession] = None,
        paginated: bool = False,
    ) -> list[MemberStatusRead]:
        query = query or QueryList()
        items = await super().get_multi(
            query=query,
            db_session=db_session,
            paginated=paginated,
        )

        data = defaultdict(list)

        for item in items:  # type: MemberStatusModel
            data[item.member_location_id.hex].append(item.member)

        member_location_items = await crud_member_location.get_multi(
            query=QueryList(
                sort=[MemberLocationModel.created_at.asc()]
            ),
        )

        result = [
            MemberStatusRead(
                member_location=member_location,
                member_list=data.get(member_location.id.hex, []),
            )
            for member_location in member_location_items
        ]
        return result

    async def handler_member_status(
        self,
        create_item: MemberStatusCreate,
        db_session: AsyncSession,
    ) -> tuple[MemberModel, MemberLocationModel]:
        member = await crud_member.get(item_id=create_item.member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='member not exist.',
            )

        member_location = await crud_member_location.get(
            item_id=create_item.member_location_id,
        )

        if not member_location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='member not exist.',
            )

        instance = await self.get(
            item_id=create_item.member_id,
            db_session=db_session,
        )
        if instance:
            if create_item.status:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'已在{instance.member_location.name}地點!'
                )
            elif create_item.member_location_id != instance.member_location_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'請從{instance.member_location.name}離開!'
                )

            await db_session.delete(instance)
        elif not create_item.status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'尚未進入任何地點!',
            )
        else:
            db_obj = self.model.from_orm(create_item)
            db_session.add(db_obj)

        return member, member_location

    async def create(
        self,
        create_item: MemberStatusCreate,
        db_session: Optional[AsyncSession] = None,
    ) -> MemberStatusCreatedRead:
        db_session = db_session or self.db.session
        member, member_location = await self.handler_member_status(
            create_item=create_item,
            db_session=db_session,
        )
        member_record = MemberRecordModel(
            status=create_item.status,
            member_location_id=member_location.id,
            member_location_name=member_location.name,
            member_location_image=member_location.image,
            member_id=member.id,
            member_name=member.name,
            member_phone=member.phone,
            member_company=member.company,
            member_job_title=member.job_title,
            member_image=member.image,
        )

        member_record = await crud_member_record.create(
            create_item=member_record,
            db_session=db_session,
        )

        member_status = MemberStatusCreatedRead(
            status=create_item.status,
            member=MemberRead.from_orm(member),
            member_location=MemberLocationRead.from_orm(member_location),
            created_at=member_record.created_at,
        )
        return member_status


crud_member_location = CRUDMemberLocation(model=MemberLocationModel)
crud_member = CRUDMember(model=MemberModel)
crud_member_record = CRUDMemberRecord(model=MemberRecordModel)
crud_member_status = CRUDMemberStatus(model=MemberStatusModel)
