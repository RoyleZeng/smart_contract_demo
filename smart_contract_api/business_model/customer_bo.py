from datetime import datetime
from uuid import UUID
from asyncpg import Connection

from smart_contract_api.business_model.management_bo import ManagementBO
from smart_contract_api.business_model.smart_contract import BikeCrankToken
from smart_contract_api.data_access_object.customer import ManagementDao
from smart_contract_api.lib.base_exception import NotFoundException, ForbiddenException
from smart_contract_api.data_access_object import default_connection, get_dao_factory
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.schema.auth import User, RegisterAccount, Role
from smart_contract_api.schema.customer import VerifyProductRequest
from smart_contract_api.schema.smart_contract import ProductData


class CustomerBO:
    @default_connection(get_dao_factory())
    async def _get_user(self, connection: Connection, user_id: UUID):
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        return await dao.query_user_by_id(user_id=user_id)

    @default_connection(get_dao_factory())
    async def _get_db_product(self, connection: Connection, product_token: str):
        dao = ManagementDao(connection=connection, operator=None)
        return await dao.get_product(product_token=product_token)

    @default_connection(get_dao_factory())
    async def verify_product(self, connection: Connection, request: VerifyProductRequest, token: UUID) -> ProductData:
        if not (user := await self._get_user(connection=connection, user_id=token)):
            raise ForbiddenException(message='Not found user')
        manage_bo = ManagementBO()
        eth_bo = BikeCrankToken()
        token_info = manage_bo.verify_token(product_token=request.product_token, barcodes=request.barcodes)
        db_product = await self._get_db_product(connection=connection, product_token=request.product_token)
        if db_product['owner'] == user['id'] or db_product['owner'] is None:
            contract_part = eth_bo.get_data(product_id=token_info['product_id'])
            return contract_part
        else:
            raise ForbiddenException(message="Product not in yor account")
