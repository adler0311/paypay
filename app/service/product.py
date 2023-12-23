from datetime import date, datetime
from typing import Union

from pydantic import BaseModel

from app.domain.product import ProductSize
from service.utils import get_chosung


class ProductCreate(BaseModel):
    category: str
    price: int
    cost: int
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: ProductSize

    def to_dict(self):
        result = self.model_dump()
        result["size"] = result["size"].name
        result["name_chosung"] = get_chosung(result["name"])
        return result


class ProductUpdate(BaseModel):
    category: str | None = None
    price: int | None = None
    cost: int | None = None
    name: str | None = None
    description: str | None = None
    barcode: str | None = None
    expiration_date: date | None = None
    size: ProductSize | None = None


def is_chosung_only(s):
    chosung_list = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]
    for char in s:
        if char not in chosung_list:
            return False
    return True
