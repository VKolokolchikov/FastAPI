from fastapi import APIRouter, Depends, status

from app.schemas import ConfigCreateSchema, ConfigUpdateSchema, UserAuthorized
from app.services import ConfigService
from app.routes.dependecy.permissions import ONLY_AUTHENTICATED


config_router = APIRouter(prefix='/config')
config_service = ConfigService()


@config_router.get('/', response_model=ConfigCreateSchema)
async def ep_get_user_config(user: UserAuthorized = Depends(ONLY_AUTHENTICATED)):
    """Get config"""
    return await config_service.get_obj(user.id)


@config_router.patch('/', status_code=status.HTTP_200_OK)
async def ep_update_user_config(
        config_data: ConfigUpdateSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Update config"""
    return await config_service.update(user.id, config_data.dict())
