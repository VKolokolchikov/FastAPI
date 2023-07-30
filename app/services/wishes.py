from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.services.base import BaseService
from app.schemas import WishListSchema
from app.models import WishListModel, WishItemModel
from app.sql.cte import can_see_friends_or_wish_cte, can_see_private_wish


class WishListService(BaseService):
    model = WishListModel

    @staticmethod
    def get_result(data: list | dict, list_: bool = False):
        if list_:
            return [WishListSchema(**wish) for wish in data]
        return WishListSchema(**data)

    async def get_wish_list(self, _id: int, *, session: AsyncSession | None = None, list_: bool = False, **kwargs):
        """Get wish list"""

        pk = 'owner_id' if list_ else 'id'

        stmt = (
            select(self.model).options(
                joinedload(self.model.items.and_(
                    WishItemModel.is_actual.is_(True)
                )))
            .where(getattr(self.model, pk) == _id, self.model.is_deleted.is_(False))
        )

        if kwargs.get('can_see_private_wish') is False:
            stmt = stmt.where(self.model.is_private.is_(False))

        result = (await self.manager.to_execute(stmt, session=session)).unique().scalars()

        if not list_:
            return self.get_result(jsonable_encoder(result.one()))

        return self.get_result(jsonable_encoder(result.all()), list_)

    async def get_owner_id(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        """Get owner wishes id """

        stmt = select(WishListModel.owner_id).where(WishListModel.id == _id)
        return await self.manager.get_object(stmt, session=session)

    async def can_edit_wish(self, wish_list_id: int, user_id: int, *, session: AsyncSession | None = None, **kwargs):
        """Check CRUD permission"""

        stmt = select(WishListModel).where(WishListModel.id == wish_list_id, WishListModel.owner_id == user_id)
        return self.manager.get_object(stmt, session=session)

    async def can_see_base_and_private_wish(
            self,
            _id: int,
            current_user_id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Check permission"""

        can_see_wish_cte = can_see_friends_or_wish_cte(current_user_id, _id, 'can_see_wish')
        stmt = select(
            can_see_wish_cte,
            can_see_private_wish(current_user_id, _id)
        ).join(can_see_wish_cte, literal(True))
        return (await self.manager.to_execute(stmt, session=session)).one()


class WishItemService(BaseService):
    model = WishItemModel

    async def get_wish_item(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        """Get wish item"""

        stmt = (
            select(self.model)
            .join(WishListModel, self.model.wish_list_id == WishListModel.id)
            .where(self.model.id == _id)
        )
        if kwargs.get('can_see_private_wish') is False:
            stmt.where(WishListModel.is_private.is_(False))

        return jsonable_encoder(await self.manager.get_object(stmt, session=session))

    async def get_item_owner_id(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        """Get owner items id"""
        sub_stmt = select(self.model.wish_list_id).where(self.model.id == _id).scalar_subquery()
        stmt = (
            select(WishListModel.owner_id)
            .where(WishListModel.id == sub_stmt)
        )
        return await self.manager.get_object(stmt, session=session)
