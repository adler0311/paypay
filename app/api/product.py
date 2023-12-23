from __future__ import annotations

from fastapi import APIRouter, Path

from fastapi import Depends
from sqlalchemy import select, update, Result, CursorResult, delete
from sqlalchemy.orm import Session

from app.api import deps
from app.domain.product import Product
from app.service.exception import ObjectNotFound
from app.service.product import ProductCreate, ProductUpdate

router = APIRouter()


@router.post("/", status_code=201)
def create_product(product_create: ProductCreate, session: Session = Depends(dependency=deps.get_db)):
    db_product = Product(**product_create.model_dump())
    print(db_product)
    session.add(db_product)
    session.commit()
    return dict(id=db_product.id)


@router.patch("/{product_id}", status_code=200)
def update_product(
        product_id,
        product_update: ProductUpdate,
        session: Session = Depends(dependency=deps.get_db)
):
    update_stmt = update(Product).where(Product.id == product_id).values(product_update.model_dump(exclude_none=True))
    result: CursorResult = session.execute(update_stmt)
    if result.rowcount == 0:
        raise ObjectNotFound(Product.__name__, id_=product_id)
    session.commit()
    return True


@router.delete("/{product_id}", status_code=200)
def delete_product(
        product_id,
        session: Session = Depends(dependency=deps.get_db)
):
    update_stmt = delete(Product).where(Product.id == product_id)
    result: CursorResult = session.execute(update_stmt)
    if result.rowcount == 0:
        raise ObjectNotFound(Product.__name__, id_=product_id)
    session.commit()
    return True


@router.get("/", status_code=200)
def list_product(
        session: Session = Depends(dependency=deps.get_db)
):
    stmt = select(Product)
    products: list[Product] = session.scalars(stmt).all()

    return products

@router.get("/{product_id}", status_code=200)
def product_details(
        product_id,
        session: Session = Depends(dependency=deps.get_db)
):
    stmt = select(Product).where(Product.id == product_id)
    product: Product = session.scalar(stmt)
    return product