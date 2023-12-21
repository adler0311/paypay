from fastapi import APIRouter

from app.api import product

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["Product"])
