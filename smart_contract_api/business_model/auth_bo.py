from datetime import datetime
from uuid import UUID
from asyncpg import Connection
from smart_contract_api.business_model.smart_contract import BikeCrankToken
from smart_contract_api.lib.base_exception import NotFoundException
from smart_contract_api.data_access_object import default_connection, get_dao_factory
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.schema.auth import User, RegisterAccount, Role


class AuthBO:
    @staticmethod
    def _to_user(user_id: UUID, name: str, eth_address: str, eht_key: str, created_at: datetime,
                 updated_at: datetime, phone: str, birthday: str, address: str, email: str, role: Role) -> User:
        return User(token=user_id, name=name, _eth_address=eth_address, _eht_key=eht_key, created_at=created_at,
                    updated_at=updated_at, phone=phone, birthday=birthday, address=address, email=email, role=role)

    @default_connection(get_dao_factory())
    async def get_dealer(self, connection: Connection, phone: str, password: str) -> User:
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        if record := await dao.query_user(phone=phone, password=password):
            return self._to_user(user_id=record['id'], name=record['name'], eth_address=record['eth_address'],
                                 eht_key=record['eht_key'], phone=record['phone'], email=record['email'],
                                 birthday=record['birthday'], address=record['address'], role=record['role'],
                                 created_at=record['created_at'],
                                 updated_at=record['updated_at'])
        else:
            raise NotFoundException(message=f'user not found name: {phone}, phone or password error')

    async def insert_dealer(self, request: RegisterAccount) -> User:
        dao: AuthDao
        eth_bo = BikeCrankToken()
        account = eth_bo.create_user_account()
        async with get_dao_factory().create_daos(AuthDao, transaction=True) as [dao]:
            record = await dao.insert_user(
                name=request.name, password=request.password, eth_address=account.address, eht_key=account.private_key,
                phone=request.phone, email=request.email, address=request.address, birthday=request.birthday,
            )
        return self._to_user(user_id=record['id'], name=record['name'], eth_address=record['eth_address'],
                             eht_key=record['eht_key'], phone=record['phone'], email=record['email'],
                             birthday=record['birthday'], address=record['address'], role=record['role'],
                             created_at=record['created_at'],
                             updated_at=record['updated_at'])
