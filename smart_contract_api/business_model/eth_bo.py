from base64 import b64decode
from datetime import datetime
from typing import Optional
from uuid import UUID
from jose import jwt
from asyncpg import Connection
from smart_contract_api.lib.base_exception import ForbiddenException
from smart_contract_api.data_access_object import get_dao_factory, default_connection
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.lib.setting import EnvironmentSettings
from smart_contract_api.schema.eth import ProductInfo
from smart_contract_api.config import get_settings

Setting = get_settings()


class JwtETHKey(EnvironmentSettings):
    jwt_public_key: str
    jwt_private_key: Optional[str]

    def get_public_key(self) -> bytes:
        return b64decode(
            bytes(self.jwt_public_key, 'utf-8'))

    def get_private_key(self) -> bytes:
        return b64decode(
            bytes(self.jwt_private_key, 'utf-8')) if self.jwt_private_key else None


class ETHBo:
    def __init__(self):
        self.key = JwtETHKey()
        self.ISS = 'Phoenix'
        self.ALGORITHM = 'RS256'
        self.private_key = self.key.get_private_key()
        self.public_key = self.key.get_public_key()

    def _generate_jwt_token(self, claims: dict, user_id: str):
        if not self.private_key:
            raise ValueError('The private key is required')
        iat = datetime.now().timestamp()
        expired_time = iat + 3600000
        common_claims = {
            "sub": user_id,
            'iss': self.ISS,
            'iat': int(iat),
            'exp': int(iat + expired_time),
        }
        claims.update(common_claims)
        return jwt.encode(claims, self.private_key, algorithm=self.ALGORITHM)

    @default_connection(get_dao_factory())
    async def _get_user(self, connection: Connection, user_id: UUID):
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        return await dao.query_user_by_id(user_id=user_id)

    async def create_product_token(self, product_info: ProductInfo, user_token: str):
        if await self._get_user(user_id=user_token):
            return self._generate_jwt_token(claims=product_info.dict(), user_id=user_token)
        else:
            raise ForbiddenException(message=f'Token: {user_token} is not correct')

    def decode_product_token(self, token):
        return jwt.decode(token, self.public_key)


if __name__ == '__main__':
    e = ETHBo()
    product = ProductInfo(barcode=['12q', '23b'], manufacture='testing1a')
    da = e.create_encode_product_token(product_info=product, user_id='zxcvbnjhgfdfyui')
    print(da)
    ta = e.decode_product_token(token=da)
    print(ta)
