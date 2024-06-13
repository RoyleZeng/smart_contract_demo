from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from smart_contract_api.business_model.management_bo import ManagementBO
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response
from smart_contract_api.lib.logger import APILog
from smart_contract_api.schema.management import UploadProduct

router = APIRouter(route_class=APILog)
_authorization = APIKeyHeader(name='Authorization', scheme_name="Authorization")


@router.post('/uploadProductionData', responses={404: {'model': ExceptionResponse}}, response_model=SingleResponse)
async def upload_production_data(request: UploadProduct, token=Depends(_authorization)):
    user = await ManagementBO().upload_production_data(request=request, token=token)
    return to_json_response(SingleResponse(result=user))
