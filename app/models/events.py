"""Events related models"""

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.mixins import BaseIntIDMixin
from app.const import EventsType


class EventModel(BaseIntIDMixin, Base):
    __tablename__ = 'event'

    name = Column(String(200), nullable=False)
    event_type = Column(String(100), nullable=False, default=EventsType.SINGLE)

    celebrating_person_id = Column(
        'celebrating_person_id', BigInteger, ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True
    )

    comment = Column(String(500), nullable=True)
    start_event_time = Column(DateTime, nullable=False)
    notification_time = Column(Time, nullable=True)
    postponement_time = Column(DateTime, nullable=True)
    crontab = Column(String(50), nullable=True)
    created_by = Column('created_by', BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)

    created = relationship("UserModel", foreign_keys=[created_by])
    celebrating_person = relationship("UserModel", foreign_keys=[celebrating_person_id])
