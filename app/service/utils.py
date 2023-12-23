import base64

from cryptography.fernet import Fernet
from pydantic import Field
from pydantic.v1.generics import GenericModel
from sqlalchemy import Select

from domain.product import Product

secret_key = Fernet.generate_key()
f = Fernet(secret_key)


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
        return {"count": len(items), "next_cursor": self.next_cursor, "items": items}

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
