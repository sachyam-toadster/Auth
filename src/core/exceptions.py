# src/core/exceptions.py
from typing import Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request


class BooklyException(Exception):
    status_code: int = 400
    error_code: str = "bookly_error"
    message: str = "Something went wrong"

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message
        super().__init__(self.message)


class UserAlreadyExists(BooklyException):
    status_code = 403
    error_code = "user_exists"
    message = "User with email already exists"


class UserNotFound(BooklyException):
    status_code = 404
    error_code = "user_not_found"
    message = "User not found"


class InvalidCredentials(BooklyException):
    status_code = 400
    error_code = "invalid_credentials"
    message = "Invalid email or password"


class InvalidToken(BooklyException):
    status_code = 401
    error_code = "invalid_token"
    message = "Token is invalid or expired"


class AccessTokenRequired(BooklyException):
    status_code = 401
    error_code = "access_token_required"
    message = "Access token is required"


class RefreshTokenRequired(BooklyException):
    status_code = 403
    error_code = "refresh_token_required"
    message = "Refresh token is required"


class InsufficientPermission(BooklyException):
    status_code = 403
    error_code = "insufficient_permissions"
    message = "You do not have permission to perform this action"


class BookNotFound(BooklyException):
    status_code = 404
    error_code = "book_not_found"
    message = "Book not found"


class TagNotFound(BooklyException):
    status_code = 404
    error_code = "tag_not_found"
    message = "Tag not found"


class TagAlreadyExists(BooklyException):
    status_code = 409
    error_code = "tag_exists"
    message = "Tag already exists"


class AccountNotVerified(BooklyException):
    status_code = 403
    error_code = "account_not_verified"
    message = "Account not verified. Please verify your email."


