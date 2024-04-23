from uuid import UUID
from asyncpg.protocol.protocol import Record
from smart_contract_api.data_access_object import BaseDao


class AuthDao(BaseDao):
    async def insert_user(self, name: str, password: str, eth_address: str, eht_key: str) -> Record:
        return await self.connection.fetchrow(
            '''
            INSERT INTO user_account (name, password, eth_address, eht_key)
            VALUES ($1, $2, $3, $4)
            RETURNING *;
            ''', name, password, eth_address, eht_key
        )

    async def query_user(self, name: str, password: str) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM user_account 
            WHERE name=$1 AND password=$2
            ''', name, password
        )

    async def query_user_by_id(self, user_id: UUID) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM user_account 
            WHERE id=$1
            ''', user_id
        )
