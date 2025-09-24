from pydantic import BaseModel

from shared.db.models import CartItem


class AddCartItemSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class UpdateCartItemSchema(BaseModel):
    quantity: int
    
    
def serialize_cart_item(item: CartItem):
    return {
        "id": item.id,
        "cart_id": item.cart_id,
        "product_id": item.product_id,
        "quantity": item.quantity,
        "price_snapshot": item.price_snapshot,
        "product": {
            "id": item.product.id,
            "title": item.product.title,
            "price": item.product.price,
            "img_url": item.product.img_url
        } if item.product else None
    }