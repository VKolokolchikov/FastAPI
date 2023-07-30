from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from app.models import InviteModel, UserModel
from app.schemas import InviteOutForReceiverSchema, InviteOutForSenderSchema
from app.services.base import BaseService

INVITE_ACTIONS = {
    0: {
        'backref': 'receiver',
        'foreign_key': 'sender_id',
        'schema': InviteOutForSenderSchema
    },

    1: {
        'backref': 'sender',
        'foreign_key': 'receiver_id',
        'schema': InviteOutForReceiverSchema
    },
}


class InviteService(BaseService):
    model = InviteModel

    async def get_invite_list(
            self,
            user_id: int,
            is_received: bool = True,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Get invite"""

        invite_action = INVITE_ACTIONS[is_received]
        
        stmt = (
            select(self.model)
            .options(joinedload(getattr(self.model, invite_action['backref'])))
            .where(and_(
                getattr(self.model, invite_action['foreign_key']) == user_id,
                self.model.sender_is_accepted.is_(True),
                self.model.receiver_is_accepted.is_(None),
            )))
        result = (await self.manager.to_execute(stmt, session=session)).scalars()

        return [invite_action['schema'](**jsonable_encoder(row)) for row in result]

    async def invite_is_exists(
            self,
            sender_id: int,
            receiver_id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Check invite"""
        stmt = (
            select(self.model)
            .where(
                or_(
                    and_(self.model.sender_id == sender_id, self.model.receiver_id == receiver_id),
                    and_(self.model.sender_id == receiver_id, self.model.receiver_id == sender_id),
                )
            ))

        return (await self.manager.to_execute(stmt, session=session)).scalars().one_or_none()

    async def can_update_invite(
            self,
            _id: int,
            user_id: int,
            is_received: bool = True,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Check permission"""
        goal_field = 'receiver_id' if is_received else 'sender_id'
        stmt = (select(self.model)
                .where(self.model.id == _id, getattr(self.model, goal_field) == user_id))
        return await self.manager.get_object(stmt, session=session)
