from datetime import datetime
from uuid import UUID
from asyncpg import Connection
from smart_contract_api.lib.base_exception import NotFoundException
from smart_contract_api.data_access_object import default_connection, get_dao_factory
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.schema.auth import User


class AuthBO:
    @staticmethod
    def _to_user(user_id: UUID, name: str, eth_address: str, eht_key: str, created_at: datetime,
                 updated_at: datetime) -> User:
        return User(token=user_id, name=name, _eth_address=eth_address, _eht_key=eht_key, created_at=created_at,
                    updated_at=updated_at)

    @default_connection(get_dao_factory())
    async def get_dealer(self, connection: Connection, name: str, password: str) -> User:
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        if record := await dao.query_user(name=name, password=password):
            return self._to_user(user_id=record['id'], name=record['name'], eth_address=record['eth_address'],
                                 eht_key=record['eht_key'],
                                 created_at=record['created_at'],
                                 updated_at=record['updated_at'])
        else:
            raise NotFoundException(message=f'user not found name: {name}, name or password error')

    async def insert_dealer(self, name: str, password: str) -> User:
        dao: AuthDao
        async with get_dao_factory().create_daos(AuthDao, transaction=True) as [dao]:
            record = await dao.insert_user(
                name=name, password=password, eth_address='', eht_key='')
        return self._to_user(user_id=record['id'], name=record['name'], eth_address=record['eth_address'],
                             eht_key=record['eht_key'],
                             created_at=record['created_at'],
                             updated_at=record['updated_at'])
