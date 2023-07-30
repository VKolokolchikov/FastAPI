from fastapi import APIRouter, status, Depends

from app.const import AnswerStatus
from app.errors import AlreadyExistsException
from app.routes.dependecy.permissions import ONLY_AUTHENTICATED, ALLOW_ANY_USERS
from app.schemas import (
    UserProfileCreateSchema,
    UserProfileProcessSchema,
    UserOutSchema,
    UserFriends,
    UserAuthorized,
    UserAnonymous, UserWithProfileSchema,
)

from app.services import UserService

user_router = APIRouter(prefix='/user')
user_service = UserService()


@user_router.get('/me', response_model=UserAuthorized)
async def ep_check_user_exist(
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Check user in system"""
    u = await user_service.get_count_wish_and_count_friends_user(user.id)
    return user


@user_router.post('/', response_model=dict)
async def ep_create_user(
        user_profile: UserProfileCreateSchema,
        user: UserAuthorized | UserAnonymous = Depends(ALLOW_ANY_USERS)
):
    """Create and return new user"""
    if isinstance(user, UserAuthorized):
        raise AlreadyExistsException()

    return await user_service.create({**user_profile.dict(), **user.dict()})


@user_router.patch('/', status_code=status.HTTP_200_OK)
async def ep_update_user(
        user_data: UserProfileProcessSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Update user"""
    return await user_service.update(_id=user.id, user_data=user_data.dict(skip_defaults=True))


@user_router.get('/search', response_model=list[UserOutSchema])
async def ep_get_search_users(
        part_name: str,
        _: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Search user in system"""
    return await user_service.search_user(part_name)


@user_router.get('/{_id}/friends/search', response_model=list[UserOutSchema])
async def ep_get_search_users(
        _id: int,
        part_name: str,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Search user in friends"""
    await user_service.can_see_friends(_id, current_user_id=user.id)
    return await user_service.search_user_in_friends(part_name, user_id=user.id)


@user_router.get('/{_id}', response_model=UserWithProfileSchema)
async def ep_get_user(
        _id: int,
        _: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Get user"""
    return await user_service.get_obj(_id)


@user_router.get('/{_id}/friends', response_model=UserFriends)
async def ep_get_user_info(
        _id: int,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Get users friends"""
    if _id == user.id or await user_service.can_see_friends(_id, current_user_id=user.id):
        return await user_service.get_user_friends(_id)

    return UserFriends(status=AnswerStatus.DENIED)
