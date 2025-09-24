# api/routers/order.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from shared.schemas.order import serialize_order
from shared.db.func.order import create_order, get_list_order, update_order_status


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=dict)
async def create_new_order(user_id: int, contact_name: str, contact_phone: str, address: str, delivery_method: str):
    order = await create_order(user_id, contact_name, contact_phone, address, delivery_method)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty or user not found")
    return serialize_order(order)


@router.get("/", response_model=List[dict])
async def list_orders(status: Optional[str] = None):
    orders = await get_list_order(status)
    return [serialize_order(o) for o in orders]


@router.patch("/{order_id}/status", response_model=dict)
async def change_order_status(order_id: int, status: str):
    order = await update_order_status(order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return serialize_order(order)
