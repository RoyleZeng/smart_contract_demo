from asyncpg import Connection
import base64
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from smart_contract_api.business_model.smart_contract import BikeCrankToken
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.lib.base_exception import NotFoundException, ForbiddenException, ParameterViolationException
from smart_contract_api.data_access_object import default_connection, get_dao_factory
from smart_contract_api.data_access_object.management import ManagementDao
from smart_contract_api.lib.setting import EnvironmentSettings
from smart_contract_api.schema.auth import Role
from smart_contract_api.schema.customer import VerifyProductRequest
from smart_contract_api.schema.management import UploadProduct, ProductInfo


class DSAKey(EnvironmentSettings):
    public_key: str
    private_key: Optional[str]

    def get_public_key(self) -> dsa.DSAPublicKey:
        return serialization.load_pem_public_key(
            base64.b64decode(self.public_key)
        )

    def get_private_key(self) -> Optional[dsa.DSAPrivateKey]:
        if self.private_key:
            return serialization.load_pem_private_key(
                base64.b64decode(self.private_key),
                password=None
            )
        return None


class ManagementBO:
    def __init__(self):
        self.key = DSAKey()
        self.ISS = 'Phoenix'
        self.private_key = self.key.get_private_key()
        self.public_key = self.key.get_public_key()

    def _generate_dsa_signed_token(self, claims: dict, user_id: str):
        if not self.private_key:
            raise ValueError('The private key is required')
        iat = datetime.now().timestamp()
        common_claims = {
            "sub": user_id,
            'iss': self.ISS,
            'iat': int(iat),
        }
        claims.update(common_claims)
        token = str(claims).encode()
        signature = self.private_key.sign(
            token,
            hashes.SHA256()
        )
        signed_token = base64.b64encode(token + b'.' + signature).decode()
        return signed_token

    def _decode_dsa_signed_token(self, signed_token: str):
        if not self.public_key:
            raise ValueError('The public key is required')
        decoded_token = base64.b64decode(signed_token)
        token, signature = decoded_token.rsplit(b'.', 1)
        try:
            self.public_key.verify(
                signature,
                token,
                hashes.SHA256()
            )
            claims = eval(token.decode())
            return claims
        except Exception as e:
            raise ValueError('Invalid token signature') from e

    def verify_token(self, product_token: str, barcodes: List[str]):
        product = self._decode_dsa_signed_token(signed_token=product_token)
        for barcode in barcodes:
            if barcode not in product['barcodes']:
                raise ParameterViolationException(message=f'barcodes: {barcodes} not match token')
        return product

    @default_connection(get_dao_factory())
    async def _get_and_user_check_permission(self, connection: Connection, token: UUID):
        auth_dao: AuthDao = AuthDao(connection=connection, operator=None)
        if not (user := await auth_dao.query_user_by_id(user_id=token)):
            raise NotFoundException(message='Not found user')
        if user['role'] != Role.MANUFACTURE:
            raise ForbiddenException(message='Permission error')
        return user

    async def upload_production_data(self, request: UploadProduct, token: UUID):
        eth_bo = BikeCrankToken()
        dao: ManagementDao
        async with get_dao_factory().create_daos(ManagementDao, transaction=True) as [dao]:
            user = await self._get_and_user_check_permission(connection=dao.connection, token=token)
            product_id = (await dao.get_product_id())['product_id']
            product_info = ProductInfo(product_id=product_id, barcodes=request.barcodes, manufacture=user['name'],
                                       created_at=datetime.now().timestamp())
            product_token = self._generate_dsa_signed_token(claims=product_info.dict(), user_id=str(token))
            print(product_token)
            await dao.insert_product(product_id=product_id, barcodes=request.barcodes, product_token=product_token)
            eth_bo.upload_data(product_id=product_id, barcode=request.barcodes, manufacture=user['name'],
                               product_token=product_token)


if __name__ == "__main__":
    # dsa_key = DSAKey()
    # private_key_pem = dsa_key.get_private_key_pem()
    # public_key_pem = dsa_key.get_public_key_pem()

    management_bo = ManagementBO()

    # 測試生成和解碼 token
    claims = ProductInfo(product_id=123, barcodes=["aaa"], manufacture="代工廠",
                         created_at=datetime.now().timestamp()).dict()
    user_id = "user123"

    # 生成 token
    signed_token = management_bo._generate_dsa_signed_token(claims=claims, user_id=user_id)
    print("Signed Token:", signed_token)

    # 解碼並驗證 token
    decoded_claims = management_bo._decode_dsa_signed_token(signed_token=signed_token)
    print("Decoded Claims:", decoded_claims)
