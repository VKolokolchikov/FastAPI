from datetime import date

from pydantic import BaseModel
from pydantic.fields import Field

from app.const import AnswerStatus, Gender


class UserBase(BaseModel):
    """Schema for User creation"""
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo_url: str | None = None

    class Config:
        orm_mode = True


class UserInSystem(UserBase):
    """Schema for base system User"""
    telegram_id: int = Field(alias="id")


class UserAuthorized(UserInSystem):
    """Schema for authorized user"""
    id: int


class UserAnonymous(UserInSystem):
    """Schema for anonymous user"""


class UserProfileCreateSchema(BaseModel):
    """Schema for User profile update"""
    birthday: date
    gender: Gender


class UserProfileProcessSchema(UserProfileCreateSchema):
    """Schema for User profile process"""
    photo_url: str | None = None


class UserOutSchema(UserBase):
    """Schema for User out"""
    id: int


class UserWithProfileSchema(UserOutSchema):
    """Schema for User out with profile"""
    count_friends: int
    count_wishes: int
    profile: UserProfileProcessSchema


class UserFriends(BaseModel):
    """Schema for friends User"""
    status: AnswerStatus = AnswerStatus.SUCCESS
    friends: list[UserOutSchema] | None = None
