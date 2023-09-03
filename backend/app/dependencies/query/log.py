from datetime import datetime, date
from typing import Optional
from fastapi import Query
from pydantic import EmailStr

from app.models import UserLogModel, UserModel
from app.utils.enums import UserLogEvent
from app.utils.sql_query import BaseQuery, QuerySql, SortSql


class UserLogQuery(BaseQuery):
    def __init__(
            self,
            event: UserLogEvent = Query(
                default=None,
                description=UserLogEvent.md(),
            ),
            created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='創建日期',
                alias='createdAt',
            ),
            event_sort: Optional[bool] = Query(
                default=None,
                description='排序動作',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createdAtNum',
            ),
            event_num: Optional[int] = Query(
                default=None,
                description='排序動作',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期',
                alias='createdAtSort',
            ),
    ):
        super(UserLogQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=UserLogModel.event == event,
                value=event,
                include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=UserLogModel.created_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=UserLogModel.event,
                sort=event_sort,
                num=event_num,
            ),
            SortSql(
                sql_field=UserLogModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            ),
        ])


class SuperUserLogQuery(BaseQuery):
    def __init__(
            self,
            event: UserLogEvent = Query(
                default=None,
                description=UserLogEvent.md(),
            ),
            email: Optional[EmailStr] = Query(
                default=None,
                description='信箱',
            ),
            username: str = Query(
                default=None,
                description='使用者名稱',
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
            username_num: Optional[int] = Query(
                default=None,
                description='使用者名稱',
                alias='usernameNum',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createdAtNum',
            ),
            event_sort: Optional[bool] = Query(
                default=None,
                description='排序動作',
                alias='eventSort',
            ),
            username_sort: Optional[bool] = Query(
                default=None,
                description='使用者名稱',
                alias='usernameSort',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期',
                alias='createdAtSort',
            ),
    ):
        super(SuperUserLogQuery, self).__init__()
        print(email)
        self.query_list.extend([
            QuerySql(
                expression=UserLogModel.event == event,
                value=event,
                include_none=False,
            ),
            QuerySql(
                expression=UserModel.username.ilike(f'%{username}%'),
                value=username,
                include_none=False,
            ),
            QuerySql(
                expression=UserModel.email == email,
                value=email,
                include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=UserLogModel.created_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=UserLogModel.event,
                sort=event_sort,
                num=event_num,
            ),
            SortSql(
                sql_field=UserModel.username,
                sort=username_sort,
                num=username_num,
            ),
            SortSql(
                sql_field=UserLogModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            ),
        ])
