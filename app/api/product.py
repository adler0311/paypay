from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy import select, update, CursorResult, delete, Select
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.api import deps
from app.domain.product import Product
from app.service.product import (
    ProductCreateIn,
    ProductUpdateIn,
    is_chosung_only,
    get_chosung,
    paginate,
    ProductOut,
)
from app.domain.user import User
from app.utils import CustomJSONResponse

router = APIRouter()


@router.post("/", status_code=201, response_class=CustomJSONResponse)
def create_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_create: ProductCreateIn,
    session: Session = Depends(dependency=deps.get_db),
):
    product = Product(**product_create.to_dict())
    session.add(product)
    session.commit()
    return dict(id=product.id)


@router.patch("/{product_id}", status_code=200, response_class=CustomJSONResponse)
def update_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_id,
    product_update: ProductUpdateIn,
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
    search_keyword: str | None = None,
    cursor: str | None = None,
    limit: int = 10,
    session: Session = Depends(dependency=deps.get_db),
):
    query: Select = select(Product).order_by(Product.id)
    if search_keyword is not None:
        if is_chosung_only(search_keyword):
            chosung_keyword = get_chosung(search_keyword)
            query: Select = query.where(
                Product.name_chosung.like(f"%{chosung_keyword}%")
            )
        else:
            query: Select = query.where(Product.name.like(f"%{search_keyword}%"))
    return paginate(session, query, limit, cursor)


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
    return ProductOut.model_validate(product)
