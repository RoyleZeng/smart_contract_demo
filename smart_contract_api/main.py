from asyncpg import IntegrityConstraintViolationError, ForeignKeyViolationError
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from lib.logger import error_log_handler, disable_mangum_logger
from lib.setting import EnvironmentParameter
from lib.base_exception import (exception_to_json_response, UniqueViolationException, ParameterViolationException,
                                add_exception_handler, use_route_names_as_operation_ids)

base_env = EnvironmentParameter()

_fastapi = {
    'title': 'HST V3 API',
    'version': base_env.version,
    'openapi_url': '/spec/swagger.json',
    'docs_url': '/spec/doc'
}

_middleware = {
    'allow_origins': '*',
    'allow_credentials': True,
    'allow_methods': ['GET', 'POST', 'PATCH', 'PUT'],
    'allow_headers': ['*']
}

app = FastAPI(**_fastapi)
app.add_middleware(CORSMiddleware, **_middleware)

add_exception_handler(app)

use_route_names_as_operation_ids(app)
disable_mangum_logger()


@app.exception_handler(IntegrityConstraintViolationError)
@error_log_handler
async def db_integrity_exception_handler(request, exc: IntegrityConstraintViolationError):
    return exception_to_json_response(UniqueViolationException(message=str(exc)))


@app.exception_handler(ForeignKeyViolationError)
@error_log_handler
async def db_foreignkey_exception_handler(request, exc: ForeignKeyViolationError):
    return exception_to_json_response(ParameterViolationException(message=str(exc)))


def handler(event, context):
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
