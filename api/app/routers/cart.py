# api/routers/cart.py
from fastapi import APIRouter, HTTPException
from typing import List

from shared.schemas.cart import serialize_cart_item, AddCartItemSchema, UpdateCartItemSchema
from shared.db.func.cart import (
    get_cart_items,
    add_to_cart,
    update_cart_item,
    remove_cart_item,
    get_cart_total,
)


router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/{user_id}", response_model=List[dict])
async def get_user_cart(user_id: int):
    items = await get_cart_items(user_id)
    return [serialize_cart_item(item) for item in items]


@router.post("/", response_model=dict)
async def add_item_to_cart(data: AddCartItemSchema):
    item = await add_to_cart(data.user_id, data.product_id, data.quantity)
    return serialize_cart_item(item)


@router.put("/{cart_item_id}", response_model=dict)
async def update_item(cart_item_id: int, data: UpdateCartItemSchema):
    item = await update_cart_item(cart_item_id, data.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return serialize_cart_item(item)


@router.delete("/{cart_item_id}", response_model=dict)
async def delete_item(cart_item_id: int):
    item = await remove_cart_item(cart_item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return serialize_cart_item(item)


@router.get("/{user_id}/total", response_model=int)
async def cart_total(user_id: int):
    total = await get_cart_total(user_id)
    return total
