import traceback

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from uvicorn import run as uvicorn_run
from uvicorn.config import LOGGING_CONFIG as UVICORN_DEFAULT_CONFIG

from app.middleware.auth import auth_dispatch
from app.routes.users import user_router
from app.routes.invites import invite_router
from app.routes.wishes import wist_router
from app.routes.configs import config_router
from app.routes.events import event_router
from app.settings import settings
from commons.logger import get_logger

logger = get_logger('api-server')


def start_app():
    """Start fastapi app"""
    app = FastAPI(
        docs_url='/documentation',
        redoc_url=None,
        title=settings.service_name,
        version='1',
        description=''
    )

    app.add_middleware(
        CORSMiddleware, allow_credentials=True,
        allow_headers=['*'], allow_origins=['*'], allow_methods=['*']
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth_dispatch)

    app.include_router(user_router, prefix='/api', tags=['user'])
    app.include_router(invite_router, prefix='/api', tags=['invite'])
    app.include_router(wist_router, prefix='/api', tags=['wish'])
    app.include_router(config_router, prefix='/api', tags=['config'])
    app.include_router(event_router, prefix='/api', tags=['event'])

    @app.exception_handler(Exception)
    async def exception_exception_handler(requests: Request, exc: Exception):
        logger.exception(exc, extra={
            'exception': traceback.format_exception(exc),
            'exception_handler': 'Exception',
            'url': requests.url,
        })
        return JSONResponse({'detail': 'Нет данных'}, status_code=500)

    @app.exception_handler(NoResultFound)
    async def no_result_found_exception_handler(requests: Request, exc: NoResultFound):
        logger.exception(exc, extra={
            'exception': traceback.format_exception(exc),
            'exception_handler': 'NoResultFound',
            'url': requests.url,
        })
        return JSONResponse({'detail': 'Не найдено'}, status_code=404)

    uvicorn_run(
        app=app,  # noqa
        host=settings.host,
        port=settings.port,
        log_config=UVICORN_DEFAULT_CONFIG,
    )


if __name__ == '__main__':
    start_app()
