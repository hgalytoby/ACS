from typing import Any, Generic, Optional, TypeVar
from uuid import UUID

from fastapi import HTTPException
from fastapi_async_sqlalchemy import db
from fastapi_async_sqlalchemy.middleware import DBSessionMeta
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import exc
from sqlmodel import SQLModel, func, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

from app.utils.pagination import Page
from app.utils.sql_query import QueryList

ModelType = TypeVar('ModelType', bound=SQLModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
ReadSchemaType = TypeVar('ReadSchemaType', bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType],
):
    def __init__(self, *, model: type[ModelType]):
        self.model = model
        self.db = db

    def get_db(self) -> DBSessionMeta:
        return self.db

    def get_select(self) -> Select | SelectOfScalar:
        return select(self.model)

    async def get_multi(
        self,
        query: Optional[QueryList] = None,
        db_session: Optional[AsyncSession] = None,
        paginated: bool = False,
    ) -> list[ReadSchemaType | ModelType] | Page[ReadSchemaType | ModelType]:
        query = query or QueryList()
        db_session = db_session or self.db.session
        expression = self.get_select().where(*query.query).order_by(*query.sort)
        if paginated:
            return await paginate(db_session, expression)
        response = await db_session.execute(expression)
        return response.scalars().all()

    async def get(
        self,
        *,
        item_id: UUID,
        db_session: Optional[AsyncSession] = None,
    ) -> Optional[ModelType]:
        db_session = db_session or self.db.session
        query = self.get_select().where(self.model.id == item_id)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: list[UUID],
        db_session: Optional[AsyncSession] = None,
    ) -> Optional[list[ModelType]]:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_first(
        self,
        *,
        db_session: Optional[AsyncSession] = None,
        query: Optional[QueryList] = None,
    ) -> ModelType | ReadSchemaType:
        db_session = db_session or self.db.session
        query = query or QueryList()
        response = await db_session.execute(
            self.get_select().where(*query.query),
        )
        return response.scalars().first()

    async def get_count(
        self,
        db_session: Optional[AsyncSession] = None,
    ) -> int:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def create(
        self,
        *,
        create_item: CreateSchemaType | ModelType,
        db_session: Optional[AsyncSession] = None,
        commit: bool = True,
    ) -> ModelType:
        db_session = db_session or self.db.session
        db_obj = self.model.from_orm(create_item)
        instance = await self.save(
            instance=db_obj,
            db_session=db_session,
            commit=commit,
        )
        return instance

    async def update(
        self,
        *,
        current_item: ModelType,
        update_item: UpdateSchemaType | dict[str, Any] | ModelType,
        db_session: Optional[AsyncSession] = None,
    ) -> ModelType:
        db_session = db_session or self.db.session
        if isinstance(update_item, dict):
            update_item = update_item
        else:
            update_item = update_item.dict(exclude_unset=True)
        for field, _ in current_item:
            if field in update_item:
                setattr(current_item, field, update_item[field])
        instance = await self.save(instance=current_item, db_session=db_session)
        return instance

    async def destroy(
        self,
        *,
        item_id: UUID | str,
        db_session: Optional[AsyncSession] = None,
    ) -> ModelType:
        db_session = db_session or self.db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id == item_id)
        )
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def save(
        self,
        instance: ModelType,
        db_session: Optional[AsyncSession] = None,
        refresh: bool = False,
        commit: bool = True,
    ) -> ModelType:
        db_session = db_session or self.db.session
        try:
            db_session.add(instance)
            if commit:
                await db_session.commit()
        except exc.IntegrityError as e:
            print(f'e: {e}')
            await db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail='Resource already exists',
            )
        if refresh:
            await db_session.refresh(instance)
        return instance
