from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from smart_contract_api.business_model.eth_bo import ETHBo
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response
from smart_contract_api.lib.logger import APILog
from smart_contract_api.schema.eth import ProductInfo

router = APIRouter(route_class=APILog)

_authorization = APIKeyHeader(name='Authorization', scheme_name="Authorization")


@router.post('/product', responses={404: {'model': ExceptionResponse}}, response_model=SingleResponse[str])
async def create_product_token(request: ProductInfo,
                               token=Depends(_authorization)):
    token = await ETHBo().create_product_token(product_info=request, user_token=token)
    return to_json_response(SingleResponse(result=token))


@router.get('/account', responses={404: {'model': ExceptionResponse}}, response_model=dict)
async def get_user_wallet_account(token=Depends(_authorization)):
    return {"token": token}
