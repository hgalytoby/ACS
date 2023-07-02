from datetime import datetime, date
from typing import Optional
from fastapi import Query
from pydantic import EmailStr

from app.models import UserModel
from app.utils.sql_query import BaseQuery, QuerySql, SortSql


class UserQuery(BaseQuery):
    def __init__(
            self,
            email: Optional[EmailStr] = Query(
                default=None,
                description='信箱',
            ),
            username: Optional[str] = Query(
                default=None,
                description='排序使用者名字',
            ),
            is_active: Optional[bool] = Query(
                default=None,
                description='啟用',
                alias='isActive',
            ),
            is_superuser: Optional[bool] = Query(
                default=None,
                description='超級使用者',
                alias='isSuperuser'
            ),
            is_verified: Optional[bool] = Query(
                default=None,
                description='驗證',
                alias='isVerified',
            ),
            created_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='創建日期',
                alias='createdAt',
            ),
            updated_at: Optional[tuple[datetime | date, datetime | date]] = Query(
                default=None,
                description='結束日期',
                alias='updateAt',
            ),
            email_num: Optional[int] = Query(
                default=None,
                description='排序信箱順序',
                alias='emailNum',
            ),
            username_num: Optional[int] = Query(
                default=None,
                description='排序使用者名稱順序',
                alias='usernameNum',
            ),
            is_active_num: Optional[int] = Query(
                default=None,
                description='排序啟用順序',
                alias='isActiveNum',
            ),
            is_superuser_num: Optional[int] = Query(
                default=None,
                description='排序超級使用者順序',
                alias='isSuperuserNum',
            ),
            is_verified_num: Optional[int] = Query(
                default=None,
                description='排序驗證順序',
                alias='isVerifiedNum',
            ),
            created_at_num: Optional[int] = Query(
                default=None,
                description='排序創建日期順序',
                alias='createdAtNum',
            ),
            updated_at_num: Optional[datetime] = Query(
                default=None,
                description='排序更新結束順序',
                alias='updatedAtNum',
            ),
            email_sort: Optional[bool] = Query(
                default=None,
                description='排序信箱',
                alias='emailNum',
            ),
            username_sort: Optional[bool] = Query(
                default=None,
                description='排序使用者名稱',
                alias='usernameSort',
            ),
            is_active_sort: Optional[bool] = Query(
                default=None,
                description='排序啟用',
                alias='isActiveSort',
            ),
            is_superuser_sort: Optional[bool] = Query(
                default=None,
                description='排序超級使用者',
                alias='isSuperuserSort',
            ),
            is_verified_sort: Optional[bool] = Query(
                default=None,
                description='排序驗證',
                alias='isVerifiedSort',
            ),
            created_at_sort: Optional[bool] = Query(
                default=None,
                description='排序創建日期',
                alias='createdAtSort',
            ),
            updated_at_sort: Optional[bool] = Query(
                default=None,
                description='排序更新日期',
                alias='updatedAtSort',
            ),

    ):
        super(UserQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=UserModel.email == email,
                value=email,
                include_none=False,
            ),
            QuerySql(
                expression=UserModel.username.ilike(f'%{username}%'),
                value=username, include_none=False,
            ),
            QuerySql(
                expression=UserModel.is_active == is_active,
                value=is_active, include_none=False,
            ),
            QuerySql(
                expression=UserModel.is_superuser == is_superuser,
                value=is_superuser, include_none=False,
            ),
            QuerySql(
                expression=UserModel.is_verified == is_verified,
                value=is_verified, include_none=False,
            ),
        ])
        self.convert_datetime_to_query(
            date_arr=created_at,
            sql_field=UserModel.created_at,
        )
        self.convert_datetime_to_query(
            date_arr=updated_at,
            sql_field=UserModel.updated_at,
        )
        self.sort_list.extend([
            SortSql(
                sql_field=UserModel.email,
                sort=email_sort,
                num=email_num,
            ),
            SortSql(
                sql_field=UserModel.username,
                sort=username_sort,
                num=username_num,
            ),
            SortSql(
                sql_field=UserModel.is_active,
                sort=is_active_sort,
                num=is_active_num,
            ),
            SortSql(
                sql_field=UserModel.is_superuser,
                sort=is_superuser_sort,
                num=is_superuser_num,
            ),
            SortSql(
                sql_field=UserModel.is_verified,
                sort=is_verified_sort,
                num=is_verified_num,
            ),
            SortSql(
                sql_field=UserModel.created_at,
                sort=created_at_sort,
                num=created_at_num,
            ),
            SortSql(
                sql_field=UserModel.updated_at,
                sort=updated_at_sort,
                num=updated_at_num,
            ),
        ])


class UserExistQuery(BaseQuery):
    def __init__(
            self,
            email: EmailStr = Query(description='信箱'),
    ):
        super(UserExistQuery, self).__init__()
        self.query_list.extend([
            QuerySql(
                expression=UserModel.email == email,
                value=email,
                include_none=False,
            ),
        ])
