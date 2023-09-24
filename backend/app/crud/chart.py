import asyncio
from datetime import datetime, timedelta
from operator import ge, le
from fastapi import Request
import psutil

from app.crud import crud_system_log, crud_member, crud_member_record
from app.models import MemberModel, MemberRecordModel
from app.schemas.chart import (
    HardDiskVolumeRead,
    EmailLogChartRead,
    BaseGrowthRead,
    MemberRecordHourlyCountRead,
    AllChartRead,
)
from app.utils.sql_query import DateRelatedQueryList


class ChartData:
    @classmethod
    def hard_disk_volume(cls) -> HardDiskVolumeRead:
        hdd = psutil.disk_usage('/')
        result = HardDiskVolumeRead(
            total=hdd.total // (2 ** 30),
            used=hdd.used // (2 ** 30),
            free=hdd.free // (2 ** 30),
        )
        return result

    @classmethod
    async def email_log_classification(cls) -> list[EmailLogChartRead]:
        items = await crud_system_log.chart()
        return items

    @classmethod
    async def member_growth(
            cls,
            query: DateRelatedQueryList
    ) -> list[BaseGrowthRead]:
        items = await crud_member.growth_chart(query=query)
        return items

    @classmethod
    async def new_member_growth(
            cls,
            query: DateRelatedQueryList
    ) -> list[BaseGrowthRead]:
        items = await crud_member.new_member_growth_chart(query=query)
        return items

    @classmethod
    async def member_record_growth(
            cls,
            query: DateRelatedQueryList
    ) -> list[BaseGrowthRead]:
        items = await crud_member_record.member_record_growth_chart(query=query)
        return items

    @classmethod
    async def member_record_hourly_count(
            cls,
            query: DateRelatedQueryList
    ) -> MemberRecordHourlyCountRead:
        items = await crud_member_record.member_record_hourly_count_chart(
            query=query,
        )
        return items

    @classmethod
    async def all_chart(cls, request: Request) -> AllChartRead:
        initial_time = request.state.initial_time
        diff_day = (datetime.today() - initial_time).days
        date_range = (
            datetime.today() - timedelta(days=diff_day + 30),
            datetime.today() + timedelta(days=30),
        )

        query_member, query_member_record = (
            DateRelatedQueryList(
                query=[
                    ge(model.created_at, date_range[0]),
                    le(model.created_at, date_range[1])],
                date_range=date_range,
            )
            for model in [MemberModel, MemberRecordModel]
        )

        tasks = [
            cls.email_log_classification(),
            cls.member_growth(query_member),
            cls.new_member_growth(query_member),
            cls.member_record_growth(query_member_record),
            cls.member_record_hourly_count(query_member_record),
        ]

        hard_disk_volume = cls.hard_disk_volume()
        
        (
            email_log_classification,
            member_growth,
            new_member_growth,
            member_record_growth,
            member_record_hourly_count,
        ) = await asyncio.gather(*tasks)

        result = AllChartRead(
            hard_disk_volume=hard_disk_volume,
            email_log_classification=email_log_classification,
            member_growth=member_growth,
            new_member_growth=new_member_growth,
            member_record_growth=member_record_growth,
            member_record_hourly_count=member_record_hourly_count,
        )
        return result
