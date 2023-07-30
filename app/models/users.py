"""User related models"""

from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.mixins import BigIntIDMixin, BaseIntIDMixin, UnDeletedDataMixin


class UserModel(BigIntIDMixin, UnDeletedDataMixin, Base):
    """User model"""
    __tablename__ = 'user'

    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    is_admin = Column(Boolean, default=False)

    wish_list = relationship('WishListModel', back_populates='owner')
    profile = relationship('ProfileModel', uselist=False, back_populates='owner_profile')

    sender_invites = relationship(
        'UserModel',
        secondary='invite',
        primaryjoin='user.c.id == invite.c.sender_id',
        secondaryjoin='user.c.id == invite.c.receiver_id',
        order_by='invite.c.id',
        viewonly=True
    )
    receiver_invites = relationship(
        'UserModel',
        secondary='invite',
        primaryjoin='user.c.id == invite.c.receiver_id',
        secondaryjoin='user.c.id == invite.c.sender_id',
        order_by='invite.c.id',
        viewonly=True
    )

    @hybrid_property
    def friends(self):
        return self.sender_invites + self.receiver_invites


class ProfileModel(BaseIntIDMixin, UnDeletedDataMixin, Base):
    """Profile model"""

    __tablename__ = 'profile'

    birthday = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    photo_url = Column(String(1024), nullable=True)
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)

    owner_profile = relationship(
        'UserModel',
        primaryjoin='user.c.id == profile.c.user_id',
        back_populates='profile', cascade='all, delete'
    )
