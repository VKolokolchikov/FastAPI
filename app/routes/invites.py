from fastapi import APIRouter, Depends, status

from app.errors import AlreadyExistsException, ForbiddenException, NotFoundException
from app.routes.dependecy.commons import url_invite_depends
from app.routes.dependecy.permissions import ONLY_AUTHENTICATED
from app.schemas import (
    UserAuthorized,
    InviteCreateSchema,
    InviteUpdateReceivedSchema,
    InviteUpdateSentSchema,
    InviteOutForReceiverSchema,
    InviteOutForSenderSchema,
)
from app.services import InviteService


invite_router = APIRouter(prefix='/invite')
invite_service = InviteService()


@invite_router.post('/', status_code=status.HTTP_200_OK)
async def ep_create_invite(
        invite_data: InviteCreateSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Create invite"""
    if invite_data.sender_id != user.id:
        raise ForbiddenException()

    if await invite_service.invite_is_exists(**invite_data.dict()):
        raise AlreadyExistsException()

    return await invite_service.create(invite_data.dict())


@invite_router.patch('/{invite_type}/{_id}', status_code=status.HTTP_200_OK)
async def ep_update_received_invite(
        _id: int,
        invite_update_data: InviteUpdateReceivedSchema | InviteUpdateSentSchema,
        is_received: bool = Depends(url_invite_depends),
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Update invite"""
    await invite_service.can_update_invite(_id=_id, user_id=user.id, is_received=is_received)
    return await invite_service.update(_id, invite_update_data.dict())


@invite_router.get(
    '/{invite_type}/list/{user_id}', response_model=list[InviteOutForReceiverSchema | InviteOutForSenderSchema]
)
async def ep_get_user_received_invite(
        user_id: int,
        is_received: bool = Depends(url_invite_depends),
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Get invite"""
    if user_id == user.id:
        return await invite_service.get_invite_list(user_id=user_id, is_received=is_received)
    raise NotFoundException()
