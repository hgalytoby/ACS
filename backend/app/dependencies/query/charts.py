from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import Query, Request

from app.models import MemberRecordModel, MemberModel
from app.utils.sql_query import BaseQuery


class MemberRecordChartQuery(BaseQuery):
    def __init__(
        self,
        request: Request,
        created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
            default=None,
            description='創建日期',
            alias='createdAt',
        ),
    ):
        super(MemberRecordChartQuery, self).__init__()

        if created_at is None:
            created_at = (
                (request.state.initial_time - timedelta(days=30)).replace(microsecond=0),
                (datetime.utcnow() + timedelta(days=30)).replace(microsecond=0),
            )

        self.date_renge = created_at
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=MemberRecordModel.created_at,
        )


class MemberChartQuery(BaseQuery):
    def __init__(
        self,
        request: Request,
        created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
            default=None,
            description='創建日期',
            alias='createdAt',
        ),
    ):
        super(MemberChartQuery, self).__init__()

        if created_at is None:
            created_at = (
                (request.state.initial_time - timedelta(days=30)).replace(microsecond=0),
                (datetime.utcnow() + timedelta(days=30)).replace(microsecond=0),
            )

        self.date_renge = created_at
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=MemberModel.created_at,
        )
