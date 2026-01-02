from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status
from src.core.exceptions import BooklyException
from src.core.exceptions import BooklyException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BooklyException)
    async def bookly_exception_handler(
        request: Request, exc: BooklyException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
                "error_code": exc.error_code,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
        )
