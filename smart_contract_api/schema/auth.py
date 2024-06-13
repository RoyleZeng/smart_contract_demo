from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, PrivateAttr


class Role(str, Enum):
    MANUFACTURE = 'manufacture'
    CUSTOMER = 'customer'


class User(BaseModel):
    token: UUID
    name: str
    phone: str
    role: Role
    birthday: str
    address: str
    email: str
    _eth_address: Optional[str] = PrivateAttr()
    _eht_key: Optional[str] = PrivateAttr()
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data):
        eth_address: Optional[str] = data.pop('_eth_address', None)
        eht_key: Optional[str] = data.pop('_eht_key', None)
        super().__init__(**data)
        self._eth_address = eth_address
        self._eht_key = eht_key

    @property
    def eth_address(self):
        return self._eth_address

    @property
    def eht_key(self):
        return self._eht_key


class RegisterAccount(BaseModel):
    name: str
    password: str
    phone: str
    birthday: str
    address: str
    email: str


class ETHAccount(BaseModel):
    address: str
    private_key: str
