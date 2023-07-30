from app.errors import NotFoundException


def url_invite_depends(invite_type):
    INVITE_TYPES = {
        'received': True,
        'sent': False
    }
    if (is_received := INVITE_TYPES.get(invite_type)) is None:
        raise NotFoundException()

    return is_received
