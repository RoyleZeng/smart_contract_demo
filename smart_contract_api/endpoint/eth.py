from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response
from smart_contract_api.lib.logger import APILog

router = APIRouter(route_class=APILog)

_authorization = APIKeyHeader(name='Authorization', scheme_name="Authorization")


@router.get('/account', responses={404: {'model': ExceptionResponse}}, response_model=dict)
async def get_user_wallet_account(token=Depends(_authorization)):
    return {"token": token}
