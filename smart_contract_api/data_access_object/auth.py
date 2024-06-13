from uuid import UUID
from asyncpg.protocol.protocol import Record
from smart_contract_api.data_access_object import BaseDao


class AuthDao(BaseDao):
    async def insert_user(self, name: str, password: str, eth_address: str, eht_key: str,
                          phone: str, birthday: str, address: str, email: str) -> Record:
        return await self.connection.fetchrow(
            '''
            INSERT INTO user_account (name, password, eth_address, eht_key, phone, birthday, address, email)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING *;
            ''', name, password, eth_address, eht_key, phone, birthday, address, email
        )

    async def query_user(self, phone: str, password: str) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM user_account 
            WHERE phone=$1 AND password=$2
            ''', phone, password
        )

    async def query_user_by_id(self, user_id: UUID) -> Record:
        return await self.connection.fetchrow(
            '''
            SELECT * FROM user_account 
            WHERE id=$1
            ''', user_id
        )

    async def insert_wallet(self, user_id: UUID) -> Record:
        return await self.connection.fetchrow(
            '''
            INSERT INTO wallet ("id", "coin", "count")
            VALUES ($1, $2, $3)
            ON CONFLICT ("id", "coin") DO UPDATE SET "count" = wallet."count" + 1
            RETURNING *
            ''', user_id, 'bike_coin', 1
        )

    async def get_wallet(self, user_id: UUID) -> list[Record]:
        return await self.connection.fetch(
            '''
            SELECT * FROM wallet WHERE id=$1
            ''', user_id
        )
