"""Configuration related models"""

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.mixins import BaseIntIDMixin, UnDeletedDataMixin
from app.const import CanSeeFriends, CanSeeWish


class ConfigModel(BaseIntIDMixin, UnDeletedDataMixin, Base):
    """Config model"""
    __tablename__ = 'config'

    can_see_friends = Column(Integer, default=CanSeeFriends.ALL_MEMBERS)
    can_see_wish = Column(Integer, default=CanSeeWish.ONLY_FRIENDS)
    send_notification_to_telegram = Column(Boolean, default=True, nullable=True)
    user_id = Column('user_id', BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)

    user = relationship("UserModel", foreign_keys=[user_id])

    list_available_users = relationship(
        'UserModel',
        secondary='can_see_private_wish',
        primaryjoin='config.c.user_id == can_see_private_wish.c.owner_id',
        secondaryjoin='user.c.id == can_see_private_wish.c.available_user_id',
        order_by='can_see_private_wish.c.id',
        viewonly=True
    )
