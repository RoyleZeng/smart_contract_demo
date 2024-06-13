from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from smart_contract_api.business_model.customer_bo import CustomerBO
from smart_contract_api.business_model.management_bo import ManagementBO
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response
from smart_contract_api.lib.logger import APILog
from smart_contract_api.schema.customer import VerifyProductRequest
from smart_contract_api.schema.management import UploadProduct
from smart_contract_api.schema.smart_contract import ProductData

router = APIRouter(route_class=APILog)
_authorization = APIKeyHeader(name='Authorization', scheme_name="Authorization")


@router.post('/verifyProduct', responses={404: {'model': ExceptionResponse}},
             response_model=SingleResponse[ProductData])
async def verify_product(request: VerifyProductRequest, token=Depends(_authorization)):
    user = await CustomerBO().verify_product(request=request, token=token)
    return to_json_response(SingleResponse(result=user))
