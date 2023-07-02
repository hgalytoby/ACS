from datetime import datetime, date
from operator import ge, le
from typing import Any, Optional
from pydantic import BaseModel, Field
from sqlalchemy.sql.elements import UnaryExpression, BinaryExpression


class BaseQuery:
    def __init__(self):
        self.query_list: list[QuerySql] = []
        self.sort_list: list[SortSql] = []

    def convert_datetime_to_query(
            self,
            sql_field: datetime | date,
            date_arr: Optional[tuple[datetime | date, datetime | date]] = None,
    ):
        if not date_arr:
            return
        start_date, end_date = date_arr[0], date_arr[1]
        if start_date:
            if isinstance(start_date, datetime):
                print(start_date.date(), start_date.time())
                start_date = datetime.strptime(f'{start_date.date()} {start_date.time()}', '%Y-%m-%d %H:%M:%S')
            self.query_list.append(
                QuerySql(
                    expression=ge(sql_field, start_date),
                    value=start_date,
                    include_none=False,
                ),
            )
        if end_date:
            if isinstance(end_date, datetime):
                end_date = datetime.strptime(f'{end_date.date()} {end_date.time()}', '%Y-%m-%d %H:%M:%S')
            self.query_list.append(
                QuerySql(
                    expression=le(sql_field, end_date),
                    value=end_date,
                    include_none=False,
                ),
            )

    def expression(self) -> list[BinaryExpression]:
        result = []
        for q in self.query_list:
            if q.value is None and not q.include_none:
                # 如果是 Value 是 None 且 include_null 是 False 就不做搜尋。
                continue
            result.append(q.expression)
        return result

    def sort(self) -> list[UnaryExpression]:
        result = {}
        for item in self.sort_list:
            if item.sort is not None:
                if item.sort is True:
                    result[item.num] = item.sql_field.desc()
                else:
                    result[item.num] = item.sql_field.asc()
        return list(map(lambda x: result[x], sorted(result.keys())))


class QuerySql(BaseModel):
    expression: BinaryExpression | bool = Field(
        description='SQL 條件的表示式',
    )
    value: Any = Field(default=False, description='要搜尋的值')
    include_none: Optional[bool] = Field(default=False, description='是否要搜尋 None')

    class Config:
        arbitrary_types_allowed = True


class SortSql(BaseModel):
    sql_field: Any = Field(description='資料庫欄位')
    sort: Optional[bool] = Field(default=None, description='升降序')
    num: Optional[int] = Field(default=None, description='順序')


class QueryList(BaseModel):
    query: Optional[list[BinaryExpression]] = Field(default_factory=list)
    sort: Optional[list[UnaryExpression]] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class DateRelatedQueryList(QueryList):
    date_range: tuple[datetime | date, datetime | date] = Field(
        description='日期範圍',
        title='日期範圍',
    )
