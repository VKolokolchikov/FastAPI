from datetime import datetime, time
from enum import Enum

from pydantic import BaseModel

from app.const import EventsType


class EventEnum(str, Enum):
    SINGLE = EventsType.SINGLE
    BIRTHDAY = EventsType.BIRTHDAY
    BUSINESS = EventsType.BUSINESS
    ANNIVERSARY = EventsType.ANNIVERSARY
    FELICITATION = EventsType.FELICITATION


class EventBaseSchema(BaseModel):
    """Schema for Event creation"""
    name: str
    event_type: EventEnum = EventEnum.SINGLE
    celebrating_person_id: int | None = None
    comment: str | None = None
    start_event_time: datetime
    notification_time: time | None = None
    postponement_time: datetime | None = None
    crontab: str | None = None


class EventUpdateSchema(EventBaseSchema):
    ...


class EventInSchema(EventBaseSchema):
    created_by: int


class EventOutSchema(EventBaseSchema):
    id: int
    created_by: int
