from fastapi import APIRouter, status

from app.schemas.events import EventInSchema, EventOutSchema, EventUpdateSchema
from app.services.events import EventService

event_router = APIRouter(prefix='/event')
event_service = EventService()


@event_router.post('/event', response_model=EventOutSchema)
async def ep_create_event(event_data: EventInSchema):
    return await event_service.create_event(event_data.dict())


@event_router.get('{_id}', response_model=EventOutSchema)
async def ep_get_event_user(_id: int):
    return await event_service.get_event(_id)


@event_router.patch('{_id}', status_code=status.HTTP_200_OK)
async def ep_update_event(_id: int, event_data: EventUpdateSchema):
    return await event_service.update_event(_id, event_data.dict())


@event_router.get('/list/{user_id}', response_model=list[EventOutSchema])
async def ep_get_event_user(user_id: int):
    return await event_service.get_events(created_by=user_id)
