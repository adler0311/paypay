import enum

from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import declarative_base

from app.domain import Base


class ProductSize(enum.Enum):
    SMALL = "small"
    LARGE = "large"


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(length=100), nullable=False)
    price = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=100), nullable=False)
    barcode = Column(String(length=100), nullable=False)
    expiration_date = Column(Date, nullable=False)
    size = Column(Enum(ProductSize, native_enum=False), nullable=False)
