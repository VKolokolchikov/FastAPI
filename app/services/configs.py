from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, insert, bindparam, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.models import ConfigModel, CanSeePrivateWish
from commons.decorators import transaction_atomic


class ConfigService(BaseService):
    model = ConfigModel
    pk = 'user_id'

    @transaction_atomic(read_only=False)
    async def update(self, _id: int, update_obj_data: dict, *, session: AsyncSession | None = None, **kwargs):
        """Update config"""

        who_can_see_private_wish_ids = update_obj_data.pop('list_available_users')
        await super().update(_id, update_obj_data, session=session, pk='user_id', **kwargs)

        users_can_see_private_wish = [
            {
                "available_user_id": user_id,
                "owner_id": _id,
                "time_updated": datetime.now(),
            }
            for user_id in who_can_see_private_wish_ids
        ]

        # Чистим старые разрешения
        stmt = delete(CanSeePrivateWish).where(CanSeePrivateWish.owner_id == _id)
        await self.manager.to_execute(stmt, session=session, read_only=False)

        # Создаём новые разрешения
        if users_can_see_private_wish:
            stmt = insert(CanSeePrivateWish).values(
                available_user_id=bindparam('available_user_id'),
                owner_id=bindparam('owner_id'),
                time_updated=bindparam('time_updated')
            )
            await self.manager.to_execute(stmt, params=users_can_see_private_wish, session=session, read_only=False)

    async def get_obj(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        """Get user config"""

        stmt = (
            select(self.model)
            .options(joinedload(self.model.list_available_users))

            .where(self.model.user_id == _id)
        )
        result = (await self.manager.to_execute(stmt, session=session)).unique().scalars()
        return jsonable_encoder(result.one())
