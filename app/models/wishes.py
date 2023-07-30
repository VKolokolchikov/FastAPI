"""Wish related models"""

from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models import UserModel, ConfigModel
from app.models.base import Base
from app.models.mixins import BaseIntIDMixin, BigIntIDMixin, UnDeletedDataMixin


class WishListModel(BaseIntIDMixin, UnDeletedDataMixin, Base):
    """Wish model"""
    __tablename__ = 'wish_list'

    is_private = Column(Boolean, default=False)
    title = Column(String(200), nullable=False)
    description = Column(String(400), nullable=True)
    owner_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)
    owner = relationship('UserModel', back_populates='wish_list', cascade='all, delete')
    items = relationship('WishItemModel', back_populates='wish')


class WishItemModel(BigIntIDMixin, Base):
    """Wish item model"""
    __tablename__ = 'wish_item'

    title = Column(String(50), nullable=False)
    comment = Column(String(200), nullable=True)
    is_actual = Column(Boolean, default=True)
    wish_list_id = Column(BigInteger, ForeignKey('wish_list.id', ondelete='CASCADE'))
    wish = relationship('WishListModel', back_populates='items', cascade='all, delete')


class CanSeePrivateWish(BaseIntIDMixin, Base):
    __tablename__ = 'can_see_private_wish'

    owner_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)
    available_user_id = Column(BigInteger, ForeignKey('user.id', ondelete='CASCADE'), index=True)

    owner_user = relationship(
        'UserModel',
        primaryjoin=owner_id == UserModel.id,
        backref='can_see_owner',
        cascade='all, delete'
    )

    __table_args__ = (
        UniqueConstraint(owner_id, available_user_id, name="notification__uc_voter_id_birthday_person_id"),
    )
