from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, select

from app.services.base import Manager
from app.models.events import EventModel
from app.schemas.events import EventOutSchema


class EventService:
    manager = Manager()

    async def create_event(self, event_data: dict):
        return jsonable_encoder(
            await self.manager.create_object(EventModel(**event_data))
        )

    async def update_event(self, _id: int, event_data: dict):
        stmt = (
            update(EventModel)
            .where(EventModel.id == _id)
            .values(**event_data)
        )
        await self.manager.to_execute(stmt, read_only=False)

    async def get_event(self, _id):
        stmt = (
            select(EventModel)
            .where(EventModel.id == _id)
        )
        return jsonable_encoder(await self.manager.get_object(stmt))

    async def get_events(self, created_by):
        stmt = (
            select(EventModel)
            .where(EventModel.created_by == created_by)
        )
        result = (await self.manager.to_execute(stmt)).scalars()
        return [EventOutSchema(**jsonable_encoder(row)) for row in result]
