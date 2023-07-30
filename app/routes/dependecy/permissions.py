from typing import Callable, Type
from fastapi import HTTPException
from starlette.requests import Request

from app.schemas.users import UserAuthorized, UserAnonymous

from app.auth.permissions import (
    BasePermission,
    AllowAny,
    IsAuthenticated,
)


def auth_depends_factory(
        permission_classes: list[Type[BasePermission]],
) -> Callable[[Request], UserAuthorized | UserAnonymous]:
    def _dependency_func(request: Request) -> UserAuthorized | UserAnonymous:
        permissions = (permission() for permission in permission_classes)
        for permission in permissions:
            if not permission.has_permission(request):
                raise HTTPException(status_code=permission.code, detail=permission.message)
        return request.state.user
    return _dependency_func


# Base permissions
ALLOW_ANY_USERS = auth_depends_factory(
    permission_classes=[AllowAny]
)

ONLY_AUTHENTICATED = auth_depends_factory(
    permission_classes=[IsAuthenticated]
)
