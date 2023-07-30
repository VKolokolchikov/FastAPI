from fastapi import APIRouter, Depends, status

from app.schemas import (
    UserAuthorized,
    WishItemInSchema,
    WishItemUpdateSchema,
    WishItemOutSchema,
    WishListInSchema,
    WishListSchema
)
from app.services import WishListService, WishItemService
from app.schemas import WishListSchema
from app.routes.dependecy.permissions import ONLY_AUTHENTICATED
from app.errors import ForbiddenException

wist_router = APIRouter(prefix='/wish')
wish_list_service = WishListService()
wish_item_service = WishItemService()


async def get_can_see_wish_config(user_id: int, owner_id: int) -> tuple:
    can_see_wish, can_see_private_wish = (
        await wish_list_service.can_see_base_and_private_wish(current_user_id=user_id, _id=owner_id)
    )
    if not can_see_wish:
        raise ForbiddenException()

    return can_see_wish, can_see_private_wish


# Items routers
@wist_router.post('/item', response_model=WishItemOutSchema)
async def ep_create_wish_item(
        item_data: WishItemInSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Create wish item"""
    await wish_list_service.can_edit_wish(wish_list_id=item_data.wish_list_id, user_id=user.id)
    return await wish_item_service.create(item_data.dict())


@wist_router.patch('/item/{_id}', status_code=status.HTTP_200_OK)
async def ep_update_wish_item(
        _id: int,
        item_data: WishItemUpdateSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Update wish item"""
    await wish_list_service.can_edit_wish(wish_list_id=item_data.wish_list_id, user_id=user.id)
    return await wish_item_service.update(_id, item_data.dict(skip_defaults=True))


@wist_router.get('/item/{_id}', response_model=WishItemOutSchema)
async def ep_get_wish_item(
        _id: int,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Get wish item"""
    owner_id = await wish_item_service.get_item_owner_id(_id)

    can_see_private_wish = True

    if owner_id != user.id:
        can_see_wish, can_see_private_wish = await get_can_see_wish_config(user_id=user.id, owner_id=owner_id)

    return await wish_item_service.get_wish_item(_id, can_see_private_wish=can_see_private_wish)


# List routers
@wist_router.post('/', response_model=WishListSchema)
async def ep_create_wish(
        wish_data: WishListInSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Create wish"""
    wish_data = wish_data.dict() | {'owner_id': user.id}
    return await wish_list_service.create(wish_data)


@wist_router.patch('/{_id}', status_code=status.HTTP_200_OK)
async def ep_update_wish_item(
        _id: int,
        wish_list_data: WishListInSchema,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    """Update wish"""
    await wish_list_service.can_edit_wish(wish_list_id=_id, user_id=user.id)
    return await wish_list_service.update(_id, wish_list_data.dict())


@wist_router.get('/{_id}', response_model=WishListSchema)
async def ep_get_wish_list(
        _id: int,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    owner_id = await wish_list_service.get_owner_id(_id)

    can_see_private_wish = True

    if owner_id != user.id:
        can_see_wish, can_see_private_wish = await get_can_see_wish_config(user_id=user.id, owner_id=owner_id)

    return await wish_list_service.get_wish_list(_id, can_see_private_wish=can_see_private_wish)


@wist_router.get('/user/{_id}', response_model=list[WishListSchema])
async def ep_get_user_wish_list(
        _id: int,
        user: UserAuthorized = Depends(ONLY_AUTHENTICATED)
):
    can_see_private_wish = True

    if _id != user.id:
        can_see_wish, can_see_private_wish = await get_can_see_wish_config(user_id=user.id, owner_id=_id)

    return await wish_list_service.get_wish_list(_id, can_see_private_wish=can_see_private_wish, list_=True)
