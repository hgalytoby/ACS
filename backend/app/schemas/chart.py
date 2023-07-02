from pydantic import Field
from datetime import date as _date

from app.schemas.base import BaseModel
from app.utils.enums import SystemLogEvent


class HardDiskVolumeRead(BaseModel):
    total: int = Field(description='總容量', title='總容量')
    used: int = Field(description='使用量', title='使用量')
    free: int = Field(description='剩餘量', title='剩餘量')


class EmailLogChartRead(BaseModel):
    event: SystemLogEvent = Field(description='系統事件', title='系統事件')
    count: int = Field(default=0, description='總數', title='總數')


class BaseGrowthRead(BaseModel):
    date: _date = Field(description='日期', title='日期')
    count: int = Field(default=0, description='數量', title='數量')


class MemberRecordHourlyCountDataRead(BaseModel):
    hour: int = Field(description='小時', title='小時')
    count: int = Field(default=0, description='數量', title='數量')


class MemberRecordHourlyCountRead(BaseModel):
    data: list[MemberRecordHourlyCountDataRead] = Field(
        default_factory=list,
        description='每小時資料',
        title='每小時資料'
    )
    start_date: _date = Field(description='日期')
    end_date: _date = Field(description='日期')


class AllChartRead(BaseModel):
    hard_disk_volume: HardDiskVolumeRead
    email_log_classification: list[EmailLogChartRead]
    member_growth: list[BaseGrowthRead]
    new_member_growth: list[BaseGrowthRead]
    member_record_growth: list[BaseGrowthRead]
    member_record_hourly_count: MemberRecordHourlyCountRead
