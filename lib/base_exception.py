import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request
from lib.logger import error_log_handler


class BoException(Exception):
    message: str
    code: str

    def __init__(self, code: str, message: str):
        self.message = message
        self.code = code


def exception_to_json_response(b_exc: BoException) -> JSONResponse:
    return JSONResponse(
        status_code=int(int(b_exc.code) / 1000),
        content={"code": b_exc.code, "message": b_exc.message},
    )


def client_exception_to_json_response(exc) -> JSONResponse:
    error = json.loads(exc.body)
    error_code = error.get('code')
    return JSONResponse(
        status_code=exc.status,
        content={"code": error_code if error_code is not None else str(exc.status) + '000',
                 "message": error.get('message') if error_code else error.get('detail')},
    )


class UnhandledException(BoException):
    def __init__(self, code: str = '500000', message: str = "Unhandled error:"):
        super().__init__(code, message)


class NotFoundException(BoException):
    def __init__(self, code: str = '404000', message: str = "Resource not found."):
        super().__init__(code, message)


class BadRequestException(BoException):
    def __init__(self, code: str = '400000', message: str = "Bad request."):
        super().__init__(code, message)


class ParameterViolationException(BoException):
    def __init__(self, code: str = '400700', message: str = "Parameter value is not valid； "):
        super().__init__(code, message)


class ForeignKeyViolationException(BoException):
    def __init__(self, code: str = '400701',
                 message: str = "Parameter value is not a valid member; permitted: .."):
        super().__init__(code, message)


class UniqueViolationException(BoException):
    def __init__(self, code: str = '400800', message: str = "The same key existed in the database.."):
        super().__init__(code, message)


class DuplicateEntityException(BoException):
    def __init__(self, code: str = '400900', message: str = "The same entity existed in the system.."):
        super().__init__(code, message)


class RestrictionException(BoException):
    def __init__(self, code: str = '409800', message: str = "This behavior is prohibited.."):
        super().__init__(code, message)


class UnauthorizedException(BoException):
    def __init__(self, code: str = '401000', message: str = "Unauthorized."):
        super().__init__(code, message)


class ForbiddenException(BoException):
    def __init__(self, code: str = '403000', message: str = "Forbidden."):
        super().__init__(code, message)


def add_exception_handler(app: FastAPI):
    @app.exception_handler(Exception)
    @error_log_handler
    async def all_exception_handler(request: Request, exc: Exception):
        return exception_to_json_response(b_exc=UnhandledException(message=str(exc)))

    @app.exception_handler(BoException)
    @error_log_handler
    async def hy_exception_handler(request: Request, exc: BoException):
        return exception_to_json_response(b_exc=exc)

    @app.exception_handler(RequestValidationError)
    @error_log_handler
    async def validation_exception_handler(request, exc: RequestValidationError):
        return exception_to_json_response(b_exc=ParameterViolationException(message=str(exc)))

    return app


def use_route_names_as_operation_ids(app: FastAPI):
    """
    Simplify operation IDs so that generated API clients have simpler function names.
    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
