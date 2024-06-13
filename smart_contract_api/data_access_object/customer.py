from uuid import UUID
from asyncpg.protocol.protocol import Record
from smart_contract_api.data_access_object import BaseDao


class ManagementDao(BaseDao):
    async def get_product(self, product_token: str) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM product WHERE product_token = $1;
            ''', product_token
        )
