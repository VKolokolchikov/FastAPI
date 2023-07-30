"""Relationship related models"""

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models import UserModel
from app.models.base import Base
from app.models.mixins import BigIntIDMixin, UnDeletedDataMixin


class InviteModel(BigIntIDMixin, UnDeletedDataMixin, Base):
    """Invite model"""
    __tablename__ = 'invite'

    sender_is_accepted = Column(Boolean, default=True, nullable=True)
    receiver_is_accepted = Column(Boolean, nullable=True)

    sender_id = Column('sender_id', BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)
    receiver_id = Column('receiver_id', BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)

    sender = relationship(
        "UserModel",
        primaryjoin=sender_id == UserModel.id,
        backref='sender_invite'
    )
    receiver = relationship(
        "UserModel",
        primaryjoin=receiver_id == UserModel.id,
        backref='receiver_invite'
    )
