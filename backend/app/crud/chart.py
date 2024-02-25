from datetime import datetime, timedelta
from operator import ge, le
import asyncio

from fastapi import Request
import psutil

from app.crud import crud_member, crud_member_record, crud_system_log
from app.models import MemberModel, MemberRecordModel
from app.schemas.chart import (
    AllChartRead,
    BaseGrowthRead,
    ChartItem,
    ChartRead,
    MemberRecordHourlyCountRead,
)
from app.utils.enums import HardDiskVolumeLabel, SystemLogEvent
from app.utils.sql_query import DateRelatedQueryList

DISK_VAL = 2 ** 30


class ChartData:
    @classmethod
    def hard_disk_volume(cls) -> ChartRead:
        hdd = psutil.disk_usage('/')
        items = [
            ChartItem(
                label=HardDiskVolumeLabel.TOTAL,
                data=hdd.total // DISK_VAL,
            ),
            ChartItem(
                label=HardDiskVolumeLabel.USED,
                data=hdd.used // DISK_VAL,
            ),
            ChartItem(
                label=HardDiskVolumeLabel.FREE,
                data=hdd.free // DISK_VAL,
            ),
        ]
        return ChartRead(items=items, labels=HardDiskVolumeLabel.values())

    @classmethod
    async def email_log_classification(cls) -> ChartRead:
        items = await crud_system_log.chart()
        return ChartRead(
            items=[
                ChartItem(label=event, data=value) for (event, value) in items
            ],
            labels=SystemLogEvent.values(),
        )

    @classmethod
    async def member_growth(
        cls,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await crud_member.growth_chart(query=query)
        return items

    @classmethod
    async def new_member_chart(
        cls,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await crud_member.new_member_chart(query=query)
        return items

    @classmethod
    async def member_record_growth(
        cls,
        query: DateRelatedQueryList,
    ) -> list[BaseGrowthRead]:
        items = await crud_member_record.member_record_growth_chart(query=query)
        return items

    @classmethod
    async def member_record_hourly_count(
        cls,
        query: DateRelatedQueryList,
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
                    le(model.created_at, date_range[1]),
                ],
                date_range=date_range,
            )
            for model in [MemberModel, MemberRecordModel]
        )

        tasks = [
            cls.email_log_classification(),
            cls.member_growth(query_member),
            cls.new_member_chart(query_member),
            cls.member_record_growth(query_member_record),
            cls.member_record_hourly_count(query_member_record),
        ]

        hard_disk_volume = cls.hard_disk_volume()

        (
            email_log_classification,
            member_growth,
            new_member_chart,
            member_record_growth,
            member_record_hourly_count,
        ) = await asyncio.gather(*tasks)

        result = AllChartRead(
            hard_disk_volume=hard_disk_volume,
            email_log_classification=email_log_classification,
            member_growth=member_growth,
            new_member_chart=new_member_chart,
            member_record_growth=member_record_growth,
            member_record_hourly_count=member_record_hourly_count,
        )
        return result
