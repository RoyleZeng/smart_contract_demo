from asyncpg import Connection
import base64
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from datetime import datetime
from uuid import UUID
from typing import List, Optional
import qrcode
from io import BytesIO
from smart_contract_api.lib.base_exception import ForbiddenException, ParameterViolationException
from smart_contract_api.data_access_object import get_dao_factory, default_connection
from smart_contract_api.data_access_object.auth import AuthDao
from smart_contract_api.lib.setting import EnvironmentSettings
from smart_contract_api.schema.eth import ProductInfo, Wallet
from smart_contract_api.config import get_settings

Verify_Token = []

Setting = get_settings()


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


class ETHBo:
    def __init__(self):
        self.key = DSAKey()
        self.ISS = 'Phoenix'
        self.private_key = self.key.get_private_key()
        self.public_key = self.key.get_public_key()

    def _generate_dsa_signed_token(self, claims: dict, user_id: str):
        if not self.private_key:
            raise ValueError('The private key is required')
        iat = datetime.now().timestamp()
        expired_time = iat + 3600000
        common_claims = {
            "sub": user_id,
            'iss': self.ISS,
            'iat': int(iat),
            'exp': int(expired_time),
        }
        claims.update(common_claims)
        token = str(claims).encode()
        signature = self.private_key.sign(
            token,
            hashes.SHA256()
        )
        signed_token = base64.b64encode(token + b'.' + signature).decode()
        return signed_token

    @default_connection(get_dao_factory())
    async def _get_user(self, connection: Connection, user_id: UUID):
        return True
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        return await dao.query_user_by_id(user_id=user_id)

    async def create_product_token(self, product_info: ProductInfo, user_token: str):
        import random
        import string
        if await self._get_user(user_id=user_token):
            return self._generate_dsa_signed_token(claims=product_info.dict(), user_id=user_token)
        else:
            raise ForbiddenException(message=f'Token: {user_token} is not correct')

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

    @default_connection(get_dao_factory())
    async def verify_token(self, connection: Connection, product_token: str, barcodes: List[str], user_token: UUID):
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        if await self._get_user(user_id=user_token):
            if product_token not in Verify_Token:
                Verify_Token.append(product_token)
                product = self._decode_dsa_signed_token(signed_token=product_token)
                for barcode in barcodes:
                    print(product['barcode'])
                    print(barcode)
                    if barcode not in product['barcode']:
                        raise ParameterViolationException(message=f'barcodes: {barcodes} not match token')
                await dao.insert_wallet(user_id=user_token)
                return product
        else:
            raise ForbiddenException(message=f'Token: {user_token} is not correct')

    @default_connection(get_dao_factory())
    async def get_user_wallet_account(self, connection: Connection, user_token: UUID) -> list[Wallet]:
        dao: AuthDao = AuthDao(connection=connection, operator=None)
        wallet_list = await dao.get_wallet(user_id=user_token)
        return [Wallet(coin=wallet['coin'], count=wallet['count']) for wallet in wallet_list]

    def generate_qrcode(self, text: str):
        # 生成 QR 码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        # 创建图像
        img = qr.make_image(fill='black', back_color='white')

        # 将图像保存到内存中的 BytesIO 对象
        img_byte_arr = BytesIO()
        img.save(img_byte_arr)
        img_byte_arr.seek(0)
        return img_byte_arr


if __name__ == '__main__':
    import asyncio

    e = ETHBo()
    product_t = ProductInfo(barcode=['12q', '23b'], manufacture='testing1a')
    da = asyncio.run(e.create_product_token(product_info=product_t, user_token='zxcvbnjhgfdfyui'))
    print(da)
    # ta = e.verify_token(token=da)
    # print(ta)
