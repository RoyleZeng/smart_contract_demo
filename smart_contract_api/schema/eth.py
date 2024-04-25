from pydantic import BaseModel


class ProductInfo(BaseModel):
    barcode: list[str]
    manufacture: str
