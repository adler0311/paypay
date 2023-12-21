from datetime import date, datetime
from typing import Union

from pydantic import BaseModel

from app.domain.product import ProductSize


class ProductCreate(BaseModel):
    category: str
    price: int
    cost: int
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: ProductSize
