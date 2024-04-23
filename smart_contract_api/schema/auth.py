from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, PrivateAttr


class User(BaseModel):
    token: UUID
    name: str
    _eth_address: str = PrivateAttr()
    _eht_key: str = PrivateAttr()
    created_at: datetime
    updated_at: datetime

    def __init__(self, **data):
        eth_address: str = data.pop('_eth_address', None)
        eht_key: str = data.pop('_eht_key', None)
        super().__init__(**data)
        self._eth_address = eth_address
        self._eht_key = eht_key
