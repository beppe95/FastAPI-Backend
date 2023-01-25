from fastapi import status as statuscode
from fastapi.responses import JSONResponse

from .models.errors import BaseError, UnauthorizedError, ForbiddenError, BadRequestError


class BaseAuthException(Exception):
    """Base error for custom API exceptions"""
    message = "Generic error"
    code = statuscode.HTTP_401_UNAUTHORIZED
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}


class BadRequestException(BaseAuthException):
    """Base error for exceptions raised because user is unauthorized"""
    message = "Bad Request"
    model = BadRequestError


class UnauthorizedException(BaseAuthException):
    """Base error for exceptions raised because user is unauthorized"""
    message = "Unauthorized"
    model = UnauthorizedError


class ForbiddenException(BaseAuthException):
    """Base error for exceptions raised because user is unauthorized"""
    message = "Forbidden"
    code = statuscode.HTTP_403_FORBIDDEN
    model = ForbiddenError
