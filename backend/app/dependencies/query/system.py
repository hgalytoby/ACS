from datetime import datetime, date
from typing import Optional
from fastapi import Query

from app.models import SystemLogModel
from app.utils.enums import SystemLogEvent
from app.utils.sql_query import BaseQuery, QuerySql, SortSql


class SystemLogQuery(BaseQuery):
    def __init__(
            self,
            event: Optional[SystemLogEvent] = Query(
                default=None,
                description=SystemLogEvent.md(),
            ),
            created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='創建日期',
                alias='createdAt',
            ),
            event_num: Optional[int] = Query(
                default=None,
                description='排序動作',
                alias='eventNum',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createAtNum',
            ),
            event_sort: Optional[bool] = Query(
                default=None,
                description='排序動作',
                alias='eventSort',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createAtSort',
            ),
    ):
        super(SystemLogQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=SystemLogModel.event == event.value,
                value=event.value,
                include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=SystemLogModel.created_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=SystemLogModel.event,
                sort=event_sort,
                num=event_num,
            ),
            SortSql(
                sql_field=SystemLogModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            )
        ])
