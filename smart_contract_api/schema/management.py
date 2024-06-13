from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, PrivateAttr


class UploadProduct(BaseModel):
    barcodes: list[str]


class ProductInfo(BaseModel):
    product_id: int
    barcodes: list[str]
    manufacture: str
    created_at: float
