from pydantic import BaseModel


class WishItemBaseSchema(BaseModel):
    """Schema for base wish item"""
    title: str
    comment: str | None = None
    is_actual: bool = True

    class Config:
        orm_mode = True


class WishItemUpdateSchema(WishItemBaseSchema):
    """Schema for wish item update"""
    title: str | None = None
    wish_list_id: int


class WishItemInSchema(WishItemBaseSchema):
    """Schema for wish item create"""
    wish_list_id: int


class WishItemOutSchema(WishItemBaseSchema):
    """Schema for wish item out"""
    id: int


class WishListInSchema(BaseModel):
    """Schema for base wish list create"""
    is_private: bool
    title: str
    description: str | None = None

    class Config:
        orm_mode = True


class WishListSchema(WishListInSchema):
    """Schema for wish list out"""
    id: int
    items: list[WishItemOutSchema] | None = None

    class Config:
        orm_mode = True
