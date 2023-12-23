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


class ProductUpdate(BaseModel):
    category: str | None = None
    price: int | None = None
    cost: int | None = None
    name: str | None = None
    description: str | None = None
    barcode: str | None = None
    expiration_date: date | None = None
    size: ProductSize | None = None

