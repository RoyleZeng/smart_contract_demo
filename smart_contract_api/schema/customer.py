from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, PrivateAttr


class VerifyProductRequest(BaseModel):
    barcodes: list[str]
    product_token: str
