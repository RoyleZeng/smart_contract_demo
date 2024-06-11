from pydantic import BaseModel


class ProductInfo(BaseModel):
    barcode: list[str]
    manufacture: str


class Wallet(BaseModel):
    coin: str
    count: int
