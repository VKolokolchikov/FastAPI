from pydantic import BaseModel

from app.schemas.users import UserOutSchema


class InviteCreateSchema(BaseModel):
    """Schema for Invite creation"""
    sender_id: int
    receiver_id: int


class InviteUpdateReceivedSchema(BaseModel):
    """Schema for Invite update for receiver"""
    receiver_is_accepted: bool


class InviteUpdateSentSchema(BaseModel):
    """Schema for Invite update for sender"""
    sender_is_accepted: bool


class InviteOutForReceiverSchema(BaseModel):
    """Schema for Invite receiver"""
    id: int
    sender: UserOutSchema
    receiver_is_accepted: bool | None
    
    
class InviteOutForSenderSchema(BaseModel):
    """Schema for Invite processing"""
    id: int
    receiver: UserOutSchema
    receiver_is_accepted: bool | None
