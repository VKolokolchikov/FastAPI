from fastapi import Request, status

from app.schemas.users import UserAuthorized, UserAnonymous


class BasePermission:
    message: str = 'Access Denied'
    code: int = status.HTTP_403_FORBIDDEN

    def __init__(self, *args, **kwargs):
        pass

    def has_permission(self, request: Request, *args, **kwargs):
        ...


class AllowAny(BasePermission):

    def has_permission(self, request: Request, *args, **kwargs):
        return isinstance(request.state.user, (UserAuthorized, UserAnonymous))


class IsAuthenticated(BasePermission):

    def has_permission(self, request: Request, *args, **kwargs):
        return isinstance(request.state.user, UserAuthorized)


class IsAuthenticatedOrReadOnly(BasePermission):

    def has_permission(self, request: Request, *args, **kwargs):
        return isinstance(request.state.user, UserAuthorized) or request.method == 'GET'
