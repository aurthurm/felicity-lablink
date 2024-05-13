from fastapi import APIRouter

from .orders import order_routes

api = APIRouter()
api.include_router(order_routes, prefix="/orders")


