import json
import logging
import time
from functools import wraps
from typing import Callable, Optional
from fastapi import Request, Response
from fastapi.routing import APIRoute
from jose import jwt

from .setting import EnvironmentSettings


class Settings(EnvironmentSettings):
    logging_level: str = 'INFO'


def init_logger() -> logging.Logger:
    global logger
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.getLevelName(Settings().logging_level))
    return logger


logger = init_logger()


def disable_uvicorn_logger():
    logging.getLogger("uvicorn.error").disabled = True
    logging.getLogger("uvicorn.access").disabled = True


def disable_mangum_logger():
    logging.getLogger("mangum").disabled = True
    logging.getLogger("mangum.lifespan").disabled = True


class PerfixAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['perfix'], msg), kwargs


def get_prefix_logger_adapter(perfix) -> logging.LoggerAdapter:
    return PerfixAdapter(logger, {'perfix': perfix})


class Loggable:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_prefix_logger_adapter(self.__class__.__name__)


def async_execution_time_logger_decorator(logger: logging.LoggerAdapter):
    def decorator(func):
        @wraps(func)
        async def async_timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            action = 'Took'
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as exc:
                action = f'get {exc.__class__.__name__} in'
                raise exc
            finally:
                total_time = time.perf_counter() - start_time
                logger.debug(
                    f'Function {func.__name__} {action} {total_time:.4f} seconds')

        return async_timeit_wrapper

    return decorator


def execution_time_logger_decorator(logger: logging.LoggerAdapter):
    def decorator(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            action = 'Took'
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:
                action = f'get {exc.__class__.__name__} in'
                raise exc
            finally:
                total_time = time.perf_counter() - start_time
                logger.debug(
                    f'Function {func.__name__} {action} {total_time:.4f} seconds')

        return timeit_wrapper

    return decorator


logger_request = get_prefix_logger_adapter("api-request-log")
logger_response = get_prefix_logger_adapter("api-response-log")
logger_exception = get_prefix_logger_adapter("api-exception-log")


def get_user_id(token: str) ->Optional[str]:
    try:
        claims = jwt.get_unverified_claims(token)
        return user_id if (user_id := claims.get('sub')) else claims.get('user_id')
    except Exception as e:
        return token


async def get_request_log(request: Request) -> dict:
    try:
        path = request.url.path
        method = request.method
        authorization = request.headers.get('authorization')
        api_version = request.headers.get('X-API-Version', None)

        request_log = {
            'user_id': get_user_id(authorization) if authorization else None,
            'api_version': api_version,
            'method': method,
            'path_params': request.path_params if request.path_params else None,
            'query_params': request.query_params._dict if request.query_params else None,
            'path': path,
            'body': await request.json() if await request.body() else None
        }
        return request_log
    except Exception as e:
        logger_request.warning({'message': f"Record request failed: {e}"})


def get_response_log(api_response: Response) -> dict:
    response_body = None
    try:
        if (response_content_length := int(api_response.headers.get('content-length', 0))) > 1000:
            response_body =  f'Response log failed, because response content length ({response_content_length}) > 1000'
        elif response_content_length > 0:        
            response_body = json.loads(api_response.body)
    except Exception as e:
        logger_response.warning({'message': f"Record response failed: {e}"})

    return {
        'status_code': api_response.status_code,
        'response_body': response_body
    }


def error_log_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        exc_dict = json.loads(response.body)
        status_code = int(exc_dict['code'][:3])
        if status_code >= 500:
            logger_exception.error({'message': exc_dict})
        if 400 <= status_code < 500:
            logger_exception.warning({'message': exc_dict})
        return response
    return wrapper


class APILog(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def api_route_handler(request: Request) -> Response:
            api_request_log = await get_request_log(request=request)
            logger_request.info(api_request_log)
            response: Response = await original_route_handler(request)
            api_response_log = get_response_log(api_response=response)
            logger_response.info(api_response_log)
            return response

        return api_route_handler
