from fastapi import APIRouter, Body
from pydantic import BaseModel
from smart_contract_api.lib.base_exception import ExceptionResponse, SingleResponse, to_json_response
from smart_contract_api.lib.logger import APILog
from smart_contract_api.schema.auth import User, RegisterAccount
from smart_contract_api.business_model.auth_bo import AuthBO

router = APIRouter(route_class=APILog)


class SessionToken(BaseModel):
    token: str


@router.post('/account', responses={404: {'model': ExceptionResponse}}, response_model=SingleResponse[User])
async def register_account(request: RegisterAccount):
    user = await AuthBO().insert_dealer(request=request)
    return to_json_response(SingleResponse(result=user))


@router.post('/session', responses={404: {'model': ExceptionResponse}}, response_model=SessionToken)
async def login(phone: str = Body(), password: str = Body()):
    user = await AuthBO().get_dealer(phone=phone, password=password)
    return SessionToken(token=str(user.token))
