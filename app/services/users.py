from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, or_, and_, func, literal
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from commons.decorators import transaction_atomic
from app.schemas import UserOutSchema, UserFriends, UserWithProfileSchema
from app.services.base import BaseService
from app.sql.cte import get_friends_ids_cte, can_see_friends_or_wish_cte
from app.models import ConfigModel, UserModel, WishListModel, WishItemModel


class UserService(BaseService):
    model = UserModel

    @transaction_atomic(read_only=False)
    async def create(self, user_data: dict, *, session: AsyncSession | None = None, **kwargs):
        """Create user and config"""

        user = await super(UserService, self).create(user_data, session=session, **kwargs)
        await self.manager.create_object(ConfigModel(user_id=user['id']), session=session)
        return jsonable_encoder(user)

    @transaction_atomic(read_only=True)
    async def get_obj(self, _id: int, *, session: AsyncSession | None = None, **kwargs):
        """Get user info """

        stmt = select(self.model).options(
            joinedload(self.model.profile)
        ).where(and_(self.model.id == _id, self.model.is_deleted.is_(False)))

        user = (await self.manager.to_execute(stmt, session=session)).unique().scalars().one()
        count_info = await self.get_count_wish_and_count_friends_user(_id, session=session)

        data = jsonable_encoder(user) | dict(count_info)
        return UserWithProfileSchema(**data)

    async def search_user(
            self,
            part_name: str,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        # Поиск пользователя по части имени
        stmt = select(self.model).where(or_(
            self.model.first_name.contains(part_name),
            self.model.last_name.contains(part_name),
            self.model.username.contains(part_name),
        ), self.model.is_deleted.is_(False))
        result = (await self.manager.to_execute(query=stmt, session=session)).scalars()
        return [UserOutSchema(**jsonable_encoder(row)) for row in result]

    async def search_user_in_friends(
            self,
            part_name: str,
            user_id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Search user in friend list"""

        # Поиск пользователя в друзьях по части имени
        stmt = (
            select(self.model)
            .where(
                or_(
                    self.model.first_name.contains(part_name),
                    self.model.last_name.contains(part_name),
                    self.model.username.contains(part_name),
                ),
                and_(
                    self.model.is_deleted.is_(False),
                    self.model.id.in_(select(get_friends_ids_cte(user_id)))
                ))
        )
        result = (await self.manager.to_execute(query=stmt, session=session)).scalars()
        return [UserOutSchema(**jsonable_encoder(row)) for row in result]

    async def get_user_by_telegram_id(
            self,
            telegram_id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs):
        """Get user by telegram id"""
        return await super(UserService, self).get_obj(_id=telegram_id, session=session, pk='telegram_id', **kwargs)

    async def get_user_friends(
            self,
            _id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Get friend list"""
        stmt = select(self.model).where(
            and_(self.model.is_deleted.is_(False), self.model.id.in_(select(get_friends_ids_cte(_id))))
        )
        result = (await self.manager.to_execute(stmt, session=session)).scalars().all()

        return UserFriends(friends=jsonable_encoder(result))

    async def can_see_friends(
            self,
            _id: int,
            current_user_id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        """Check permission"""
        return await self.manager.get_object(
            select(
                can_see_friends_or_wish_cte(current_user_id, _id, can_see_field='can_see_friends')
            ), session=session
        )

    async def get_count_wish_and_count_friends_user(
            self,
            _id: int,
            *,
            session: AsyncSession | None = None,
            **kwargs
    ):
        c_f = select(func.count().label('count_friends')).select_from(get_friends_ids_cte(_id)).subquery()
        c_w = (
            select(func.count(WishItemModel.id).label('count_wishes'))
            .select_from(self.model)
            .join(WishListModel, self.model.id == WishListModel.owner_id)
            .join(WishItemModel, WishListModel.id == WishItemModel.wish_list_id)
            .where(and_(UserModel.id == _id, UserModel.is_deleted.is_(False), WishListModel.is_private.is_(False)))
        ).subquery()
        stmt = select(c_f, c_w).join(c_w, literal(True))
        return (await self.manager.to_execute(stmt, session=session)).mappings().one()
