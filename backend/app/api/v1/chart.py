from fastapi import APIRouter, Request, status
from fastapi_restful.cbv import cbv

from app.crud.chart import ChartData
from app.dependencies.base import web_date_renge_params
from app.dependencies.query import (
    MemberChartQuery,
    MemberRecordChartQuery,
)
from app.schemas.chart import (
    AllChartRead,
    BaseGrowthRead,
    ChartRead,
    MemberRecordHourlyCountRead,
)
from app.utils.enums import APIAccess
from app.utils.sql_query import DateRelatedQueryList

router = APIRouter(prefix='/charts', tags=['數據圖'])


@cbv(router)
class ChartView:
    @router.get(
        '/hard-disk-volume',
        name=APIAccess.PRIVATE,
        summary='硬碟狀況',
        status_code=status.HTTP_200_OK,
    )
    def hard_disk_volume(self) -> ChartRead:
        items = ChartData.hard_disk_volume()
        return items

    @router.get(
        '/email-log-classification',
        name=APIAccess.PRIVATE,
        summary='系統日誌分類',
        status_code=status.HTTP_200_OK,
    )
    async def email_log_classification(self) -> ChartRead:
        items = await ChartData.email_log_classification()
        return items

    @router.get(
        '/member-growth',
        name=APIAccess.PRIVATE,
        summary='成員成長',
        status_code=status.HTTP_200_OK,
    )
    async def member_growth(
        self,
        query: DateRelatedQueryList = web_date_renge_params(MemberChartQuery),
    ) -> list[BaseGrowthRead]:
        items = await ChartData.member_growth(query=query)
        return items

    @router.get(
        '/new-member-chart',
        name=APIAccess.PRIVATE,
        summary='新成員成長',
        status_code=status.HTTP_200_OK,
    )
    async def new_member_growth(
        self,
        query: DateRelatedQueryList = web_date_renge_params(MemberChartQuery),
    ) -> list[BaseGrowthRead]:
        items = await ChartData.new_member_chart(query=query)
        return items

    @router.get(
        '/member-record-growth',
        name=APIAccess.PRIVATE,
        summary='成員記錄成長',
        status_code=status.HTTP_200_OK,
    )
    async def member_record_growth(
        self,
        query: DateRelatedQueryList = web_date_renge_params(
            MemberRecordChartQuery
        ),
    ) -> list[BaseGrowthRead]:
        items = await ChartData.member_record_growth(query=query)
        return items

    @router.get(
        '/member-record-hourly-count',
        name=APIAccess.PRIVATE,
        summary='進出時段紀錄',
        status_code=status.HTTP_200_OK,
    )
    async def member_record_hourly_count(
        self,
        query: DateRelatedQueryList = web_date_renge_params(
            MemberRecordChartQuery
        ),
    ) -> MemberRecordHourlyCountRead:
        items = await ChartData.member_record_hourly_count(query=query)
        return items

    @router.get(
        '/all-chart',
        name=APIAccess.PRIVATE,
        summary='全部圖表資料',
        status_code=status.HTTP_200_OK,
    )
    async def all_chart(
        self,
        request: Request,
    ) -> AllChartRead:
        items = await ChartData.all_chart(request=request)
        return items
