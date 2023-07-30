from urllib.parse import unquote

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound

from app.middleware.utils import extract_user_from_auth_data
from app.middleware.validators import validate_auth_data
from app.schemas.users import UserAnonymous, UserAuthorized
from app.services.users import UserService
from app.settings import settings
from commons.logger import get_logger

AUTH_HEADER = 'Authorization'
logger = get_logger('api-server', extra={'middleware': 'auth'})


async def get_user(auth_data: dict):
    user_service = UserService()
    try:
        user = await user_service.get_user_by_telegram_id(auth_data['id'])
    except NoResultFound as _:
        return UserAnonymous(**auth_data)
    return UserAuthorized(**jsonable_encoder(user))


async def auth_dispatch(request: Request, call_next):
    """Auth middleware"""

    auth_data = request.headers.get(AUTH_HEADER, '') or base_q
    auth_data = unquote(auth_data)

    if not validate_auth_data(auth_data=auth_data, token=settings.tg_secret_key):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'reason': "The server configuration prohibits executing a request to the endpoint"}
        )

    telegram_user = extract_user_from_auth_data(auth_data)

    request.state.user = await get_user(telegram_user)
    response = await call_next(request)
    return response
