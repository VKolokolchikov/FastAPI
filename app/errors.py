from typing import Any

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """Error that can be raised in any place of the app"""

    def __init__(self, status_code: int = None, detail: Any = None) -> None:
        super().__init__(
            status_code=status_code or self.status_code,
            detail=detail or self.detail,
        )


class AlreadyExistsException(BaseAppException):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Already exists"


class NotFoundException(BaseAppException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Not found"


class ForbiddenException(BaseAppException):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Access denied"
