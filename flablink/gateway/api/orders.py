from fastapi import APIRouter, Request

order_routes = APIRouter()

@order_routes.get("/api/orders")
async def api_orders(request: Request):
    return Orders.all()

@order_routes.post("/api/orders/resync/{uid}")
async def api_orders(uid):
    order = Orders.find(uid)
    order.update(synced=0)
    return order

