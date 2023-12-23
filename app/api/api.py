from fastapi import APIRouter

from api import auth
from app.api import product

api_router = APIRouter()
api_router.include_router(product.router, prefix="/products", tags=["Product"])
api_router.include_router(auth.router, tags=["Auth"])
