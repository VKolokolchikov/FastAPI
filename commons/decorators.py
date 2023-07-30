import functools

from app.db import get_session


def transaction_atomic(read_only=True):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            async with get_session(read_only=read_only) as session:
                result = await func(*args, session=session, **kwargs)
                await session.commit()
                return result

        return wrapped

    return wrapper
