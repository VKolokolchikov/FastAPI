from sqlalchemy import delete, update, select
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.interface import AbstractService
from commons.managers.base import Manager


class BaseService(AbstractService):
    manager = Manager()
    pk = 'id'
    deleted_field = 'is_deleted'

    async def create(self, obj: dict, *, session: AsyncSession | None = None, **kwargs):
        return jsonable_encoder(
            await self.manager.create_object(self.model(**obj), session=session, **kwargs)
        )

    async def update(self, _id: int, update_obj_data: dict, *, session: AsyncSession | None = None, **kwargs):
        pk = kwargs.get('pk') or self.pk
        stmt = update(self.model).where(getattr(self.model, pk) == _id).values(**update_obj_data)
        await self.manager.to_execute(stmt, session=session, read_only=False, **kwargs)

    async def get_obj(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        pk = kwargs.get('pk') or self.pk
        stmt = select(self.model).where(getattr(self.model, pk) == _id)
        if active_obj := getattr(self.model, self.deleted_field):
            stmt = stmt.where(active_obj.is_(False))
        return await self.manager.get_object(stmt, session=session, **kwargs)

    async def delete(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        pk = kwargs.get('pk') or self.pk
        if getattr(self.model, self.deleted_field):
            stmt = (
                update(self.model)
                .where(getattr(self.model, pk) == _id)
                .values(**{f'{self.deleted_field}': True})
            )
        else:
            stmt = delete(self.model).where(getattr(self.model, pk) == _id)

        return self.manager.to_execute(stmt, session=session, read_only=False, **kwargs)
