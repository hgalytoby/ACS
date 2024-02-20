from typing import TypeVar

from fastapi import Depends

from app.utils.sql_query import BaseQuery, DateRelatedQueryList, QueryList

QueryType = TypeVar('QueryType', bound=type[BaseQuery])


def depend(func):
    def wrapper():
        return Depends(func)

    return wrapper


def web_params(query: QueryType) -> QueryList:
    @depend
    def foo(q: query = Depends()) -> QueryList:
        return QueryList(query=q.expression(), sort=q.sort())

    return foo()


def web_date_renge_params(query: QueryType) -> DateRelatedQueryList:
    @depend
    def foo(q: query = Depends()) -> DateRelatedQueryList:
        return DateRelatedQueryList(
            query=q.expression(),
            sort=q.sort(),
            date_range=q.date_renge,
        )

    return foo()
