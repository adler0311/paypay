from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, ConfigDict

from app.domain.product import ProductSize


class ProductCreateIn(BaseModel):
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


class ProductUpdateIn(BaseModel):
    category: str | None = None
    price: int | None = None
    cost: int | None = None
    name: str | None = None
    description: str | None = None
    barcode: str | None = None
    expiration_date: date | None = None
    size: ProductSize | None = None


class ProductOut(BaseModel):
    category: str
    price: int
    cost: int
    name: str
    description: str
    barcode: str
    expiration_date: date
    size: ProductSize

    model_config = ConfigDict(from_attributes=True)


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


import base64

from cryptography.fernet import Fernet
from pydantic import Field, parse_obj_as
from pydantic.v1.generics import GenericModel
from sqlalchemy import Select
from sqlalchemy.orm import Query

from app.domain.product import Product
from app.service.product import ProductOut


def encode_id(identifier: int) -> str:
    encoded_bytes = base64.urlsafe_b64encode(str(identifier).encode())
    token = encoded_bytes.decode()
    return token


def decode_id(token: str) -> int:
    decoded_bytes = base64.urlsafe_b64decode(token)
    return int(decoded_bytes.decode())


class PaginatedResponse(GenericModel):
    count: int = Field()
    next_cursor: str | None = Field(None)
    items: list = Field()


class Paginator:
    def __init__(self, session, query, max_results, cursor):
        self.session = session
        self.query = query
        self.max_results = max_results
        self.cursor = cursor
        self.next_cursor = None

    def get_response(self):
        if self.cursor is None:
            query = self.query.limit(self.max_results + 1)
        else:
            ident = decode_id(self.cursor)
            query = self.query.where(Product.id > ident).limit(self.max_results + 1)
        items = self._get_next(query)
        return {
            "count": len(items),
            "next_cursor": self.next_cursor,
            "items": list(map(ProductOut.model_validate, items)),
        }

    def _get_next(self, query: Select) -> list[Product]:
        initial_items = [item for item in self.session.scalars(query)]
        if len(initial_items) < self.max_results + 1:
            return initial_items
        else:
            items = initial_items[:-1]
            self.next_cursor = encode_id(items[-1].id)
            return items


def paginate(session, query: Select, max_results: int, cursor: str | None):
    paginator = Paginator(session, query, max_results, cursor)
    return paginator.get_response()


def get_chosung(word):
    chosungs = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    result = ""

    for char in word:
        if "가" <= char <= "힣":
            # 유니코드 상에서 한글의 시작 부분인 '가'에서 뺀 값으로 인덱스 계산
            chosung_index = (ord(char) - ord("가")) // 588
            result += chosungs[chosung_index]
        else:
            result += char
    return result
