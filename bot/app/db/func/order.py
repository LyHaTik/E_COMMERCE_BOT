import uuid
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Order, OrderItem, CartItem, Cart
from db.connect import AsyncSessionLocal


def generate_order_number() -> str:
    """Генерация уникального номера заказа"""
    return f"ORD-{uuid.uuid4().hex[:10].upper()}"


async def create_order(user_id: int, contact_name: str, contact_phone: str, address: str, delivery_method: str):
    """Оформление заказа из корзины"""
    async with AsyncSessionLocal() as session:

        result = await session.execute(select(Cart).where(Cart.user_id == user_id))
        cart = result.scalar_one_or_none()
        if not cart:
            return None

        result = await session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart.id))
        cart_items = result.scalars().all()
        if not cart_items:
            return None

        total = sum(i.quantity * i.price_snapshot for i in cart_items)

        order = Order(
            user_id=user_id,
            order_number=generate_order_number(),
            total=total,
            delivery_method=delivery_method,
            contact_name=contact_name,
            contact_phone=contact_phone,
            address=address,
        )
        session.add(order)
        await session.flush()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                title_snapshot=item.product.title,
                price_snapshot=item.price_snapshot,
                quantity=item.quantity
            )
            session.add(order_item)

        for item in cart_items:
            await session.delete(item)

        await session.commit()
        await session.refresh(order)
        return order


async def get_list_order(status: str = None):
    """Список заказов (для админки)"""
    async with AsyncSessionLocal() as session:
        stmt = select(Order)
        if status:
            stmt = stmt.where(Order.status == status)
        else:
            stmt = stmt.where(Order.status != "COMPLETED")

        result = await session.execute(stmt)
        return result.scalars().all()


async def update_order_status(order_id: int, status: str):
    """Изменение статуса заказа"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            return None
        order.status = status
        await session.commit()
        return order
