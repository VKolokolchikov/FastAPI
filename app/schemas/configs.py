from enum import IntEnum

from pydantic import BaseModel, ValidationError, validator

from app.schemas.users import UserOutSchema
from app.const import CanSeeFriends, CanSeeWish


class CanSeeFriendsEnum(IntEnum):
    ALL_MEMBERS = CanSeeFriends.ALL_MEMBERS
    ONLY_FRIENDS = CanSeeFriends.ONLY_FRIENDS
    NOBODY = CanSeeFriends.NOBODY


class CanSeeWishEnum(IntEnum):
    ALL_MEMBERS = CanSeeWish.ALL_MEMBERS
    ONLY_FRIENDS = CanSeeWish.ONLY_FRIENDS
    NOBODY = CanSeeWish.NOBODY


class ConfigOutSchema(BaseModel):
    """Schema for out config"""
    can_see_friends: int = CanSeeFriendsEnum.ALL_MEMBERS
    can_see_wish: int = CanSeeWish.ONLY_FRIENDS


class ConfigCreateSchema(ConfigOutSchema):
    """Schema for create config"""
    list_available_users: list[UserOutSchema]


class ConfigUpdateSchema(ConfigOutSchema):
    """Schema for update config"""
    list_available_users: list[int]

    @validator("list_available_users")
    def check_list_available_users(cls, value, values):
        if values['can_see_wish'] == CanSeeWish.NOBODY and value:
            raise ValueError("Для данного ограничения не предусмотрена возможность доступа к желаниям!")
