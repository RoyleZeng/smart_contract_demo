from uuid import UUID
from asyncpg.protocol.protocol import Record
from smart_contract_api.data_access_object import BaseDao


class ManagementDao(BaseDao):
    async def get_product_id(self) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT nextval('product_id_seq'::regclass) product_id
            '''
        )

    async def insert_product(self, product_id: int, barcodes: list[str], product_token: str) -> Record:
        return await self.connection.fetchrow(
            '''
            INSERT INTO product (id, barcodes, product_token)
            VALUES ($1, $2, $3)
            RETURNING *;
            ''', product_id, barcodes, product_token
        )
