from typing import Any

from sqlalchemy import select, case, and_, or_, literal_column
from sqlalchemy.sql.elements import BinaryExpression
from app.models import InviteModel, ConfigModel, CanSeePrivateWish
from app.const import CanSeeFriends, CanSeeWish


CAN_SEE_CONST = {
    'can_see_friends': {
        'field': 'can_see_friends',
        'const': CanSeeFriends
    },
    'can_see_wish': {
        'field': 'can_see_wish',
        'const': CanSeeWish
    }
}


def get_friends_ids_cte(user_id: int):
    return (
        select(
            case([
                (InviteModel.sender_id == user_id, InviteModel.receiver_id),
                (InviteModel.receiver_id == user_id, InviteModel.sender_id),
            ]))
        .where(
            or_(InviteModel.sender_id == user_id, InviteModel.receiver_id == user_id),
            and_(InviteModel.sender_is_accepted.is_(True), InviteModel.receiver_is_accepted.is_(True))
        )
        .cte('friends_user_cte'))


def can_see_somthing_cte(
        case_params: list[tuple],
        where: list[BinaryExpression | bool],
        else_: Any | None = None,
        label: str | None = None
):
    return select(
        case(case_params, else_=else_).label(label)
    ).where(*where).cte(label)


def can_see_friends_or_wish_cte(current_user: int, user_id: int, can_see_field: str):
    const_ = CAN_SEE_CONST[can_see_field]
    case_params = [
        (and_(
            getattr(ConfigModel, const_['field']) == const_['const'].ONLY_FRIENDS,
            literal_column(f'{current_user}').not_in(select(get_friends_ids_cte(user_id)))), False),
        (getattr(ConfigModel, const_['field']) == const_['const'].NOBODY, False)
    ]
    else_ = True
    where = [ConfigModel.user_id == user_id]
    return can_see_somthing_cte(case_params, where=where, else_=else_, label='can_see_friends')


def can_see_private_wish(current_user: int, user_id: int):
    stmt = select(CanSeePrivateWish.id).where(CanSeePrivateWish.owner_id == user_id).subquery()
    case_params = [
        (and_(select(can_see_friends_or_wish_cte(current_user, user_id, 'can_see_wish')) is True,
              literal_column(f'{current_user}').in_(select(stmt))), True),
    ]
    else_ = False
    where = [ConfigModel.user_id == user_id]
    return can_see_somthing_cte(case_params, where=where, else_=else_, label='can_see_private_wish')
