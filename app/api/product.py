from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select, update, CursorResult, delete
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from app.api import deps
from app.domain.product import Product
from app.service.product import ProductCreate, ProductUpdate
from domain.user import User
from utils import CustomJSONResponse

router = APIRouter()


@router.post("/", status_code=201, response_class=CustomJSONResponse)
def create_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_create: ProductCreate,
    session: Session = Depends(dependency=deps.get_db),
):
    db_product = Product(**product_create.model_dump())
    print(db_product)
    session.add(db_product)
    session.commit()
    return dict(id=db_product.id)


@router.patch("/{product_id}", status_code=200, response_class=CustomJSONResponse)
def update_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id,
    product_update: ProductUpdate,
    session: Session = Depends(dependency=deps.get_db),
):
    update_stmt = (
        update(Product)
        .where(Product.id == product_id)
        .values(product_update.model_dump(exclude_none=True))
    )
    result: CursorResult = session.execute(update_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    session.commit()
    return True


@router.delete("/{product_id}", status_code=200, response_class=CustomJSONResponse)
def delete_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id,
    session: Session = Depends(dependency=deps.get_db),
):
    update_stmt = delete(Product).where(Product.id == product_id)
    result: CursorResult = session.execute(update_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    session.commit()
    return True


@router.get("/", status_code=200, response_class=CustomJSONResponse)
def list_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(dependency=deps.get_db),
):
    stmt = select(Product)
    products: list[Product] = session.scalars(stmt).all()

    return dict(products=products)


@router.get("/{product_id}", status_code=200, response_class=CustomJSONResponse)
def product_details(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id,
    session: Session = Depends(dependency=deps.get_db),
):
    stmt = select(Product).where(Product.id == product_id)
    product: Product | None = session.scalar(stmt)
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return product
