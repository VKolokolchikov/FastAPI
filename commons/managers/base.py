from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from commons.managers.interface import AbstractManageService


class Manager(AbstractManageService):

    def _init_session_if_needed(func):
        async def wrapper(*args, **kwargs):
            if kwargs.get('session') is None:
                async with get_session(read_only=kwargs.get('read_only') or True) as session:
                    kwargs['session'] = session
                    result = await func(*args, **kwargs)
                    await session.commit()
                    return result
            return await func(*args, **kwargs)
        return wrapper

    _init_session_if_needed = staticmethod(_init_session_if_needed)

    @staticmethod
    @_init_session_if_needed
    async def to_execute(
            query,
            params: Any | None = None,
            session: AsyncSession | None = None,
            read_only: bool = True,
            return_value: bool = True,
            **kwargs
    ):
        result = await session.execute(query, params)

        if not read_only:
            await session.flush()

        if return_value:
            return result

    @staticmethod
    async def _create(obj, session: AsyncSession, **kwargs):
        session.add(obj)
        await session.flush()
        return obj

    @_init_session_if_needed
    async def get_object(
            self, select_query,
            session: AsyncSession | None = None,
            **kwargs
    ):
        return (await session.scalars(select_query)).one()

    @_init_session_if_needed
    async def create_object(
            self, obj,
            session: AsyncSession | None = None,
            read_only: bool = False,
            **kwargs
    ):
        return await self._create(
            obj, session=session, read_only=read_only, **kwargs
        )
