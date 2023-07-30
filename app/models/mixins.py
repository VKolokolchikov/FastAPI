"""Mixin models"""

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer
from sqlalchemy import func


class DateTimeDataMixin:
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class BigIntIDMixin(DateTimeDataMixin):
    id = Column(BigInteger(), primary_key=True)


class BaseIntIDMixin(DateTimeDataMixin):
    id = Column(Integer, primary_key=True)


class UnDeletedDataMixin:
    is_deleted = Column(Boolean, nullable=False, default=False)
