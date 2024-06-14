from datetime import datetime
from typing import Optional
from uuid import UUID
from pypika import PostgreSQLQuery, Table
from asyncpg.protocol.protocol import Record
from smart_contract_api.data_access_object import BaseDao


class CustomerDao(BaseDao):
    tb_product = Table('product')

    async def get_product(self, product_token: str) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM product WHERE product_token = $1;
            ''', product_token
        )

    async def update_product(self, product_token: str, is_registered: Optional[bool] = None,
                             is_listed: Optional[bool] = None) -> Record:
        sql = PostgreSQLQuery.update(self.tb_product).where(
            self.tb_product.product_token == product_token).returning('*')
        if is_registered is not None:
            sql = sql.set(self.tb_product.is_registered, is_registered)
        if is_registered:
            sql = sql.set(self.tb_product.registered_at, datetime.now())
        if is_listed is not None:
            sql = sql.set(self.tb_product.is_listed, is_listed)
        return await self.connection.fetchrow(sql.get_sql())