from fastapi import APIRouter

from app.api import auth, product

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["Product"])
api_router.include_router(auth.router, tags=["Auth"])
