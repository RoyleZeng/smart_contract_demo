from fastapi import APIRouter, Depends, Body
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from smart_contract_api.business_model.eth_bo import ETHBo
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response, ListResponse
from smart_contract_api.lib.logger import APILog
from smart_contract_api.schema.eth import ProductInfo, Wallet

router = APIRouter(route_class=APILog)

_authorization = APIKeyHeader(name='Authorization', scheme_name="Authorization")


@router.post('/product', responses={404: {'model': ExceptionResponse}}, response_model=SingleResponse[str])
async def create_product_token(request: ProductInfo,
                               token=Depends(_authorization)):
    token = await ETHBo().create_product_token(product_info=request, user_token=token)
    return to_json_response(SingleResponse(result=token))


@router.post('/product/coin', responses={404: {'model': ExceptionResponse}}, response_model=SingleResponse[ProductInfo])
async def verify_product_token_and_get_coin(product_token: str = Body(), barcodes: list[str] = Body(),
                                            token=Depends(_authorization)):
    product = await ETHBo().verify_token(barcodes=barcodes, user_token=token, product_token=product_token)
    return to_json_response(SingleResponse(result=product))


@router.get('/account', responses={404: {'model': ExceptionResponse}}, response_model=ListResponse[Wallet])
async def get_user_wallet_account(token=Depends(_authorization)):
    product = await ETHBo().get_user_wallet_account(user_token=token)
    return to_json_response(SingleResponse(result=product))


@router.get('/generate_qrcode', responses={404: {'model': ExceptionResponse}}, response_model=dict)
def generate_qrcode(text: str):
    # 生成 QR 码
    img_byte_arr = ETHBo().generate_qrcode(text=text)
    return StreamingResponse(img_byte_arr, media_type="image/png")
