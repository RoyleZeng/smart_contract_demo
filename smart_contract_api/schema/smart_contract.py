from pydantic import BaseModel


class ProductData(BaseModel):
    id: int
    barcodes: list[str]
    manufacture: str
    is_registered: bool
    product_token: str
