from __future__ import annotations

from fastapi import APIRouter, Path

from fastapi import Depends
from sqlalchemy import select, update, Result, CursorResult, delete
from sqlalchemy.orm import Session

from app.api.deps import get_session
from app.domain.product import Product
from app.service.product import ProductCreate

router = APIRouter()


@router.post("/", status_code=201)
def create_product(product_create: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product(**product_create.model_dump())
    print(db_product)
    session.add(db_product)
    session.commit()
    return dict(id=db_product.id)