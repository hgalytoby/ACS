from datetime import date as _date
from typing import Any

from pydantic import Field

from app.schemas.base import BaseModel


class BaseGrowthRead(BaseModel):
    date: _date = Field(description='日期', title='日期')
    count: int = Field(default=0, description='數量', title='數量')


class MemberRecordHourlyCountDataRead(BaseModel):
    hour: str = Field(description='小時', title='小時')
    count: int = Field(default=0, description='數量', title='數量')


class MemberRecordHourlyCountRead(BaseModel):
    data: list[MemberRecordHourlyCountDataRead] = Field(
        default_factory=list,
        description='每小時資料',
        title='每小時資料'
    )
    start_date: _date = Field(description='日期')
    end_date: _date = Field(description='日期')


class ChartItem(BaseModel):
    label: str
    data: Any


class ChartRead(BaseModel):
    items: list[ChartItem]
    labels: list[str]


class AllChartRead(BaseModel):
    hard_disk_volume: ChartRead
    email_log_classification: ChartRead
    member_growth: list[BaseGrowthRead]
    new_member_chart: list[BaseGrowthRead]
    member_record_growth: list[BaseGrowthRead]
    member_record_hourly_count: MemberRecordHourlyCountRead
