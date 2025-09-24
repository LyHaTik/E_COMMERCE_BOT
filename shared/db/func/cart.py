from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload

from shared.db.models import Cart, CartItem, Product
from shared.db.connect import AsyncSessionLocal


async def get_cart_item(cart_item_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id == cart_item_id)
        )
        return result.scalar_one_or_none()


async def get_or_create_cart(user_id: int):
    """Возвращает корзину пользователя, если нет – создаёт"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Cart).where(Cart.user_id == user_id)
        )
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user_id)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)
        return cart


async def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    """Добавление товара в корзину"""
    async with AsyncSessionLocal() as session:
        cart = await get_or_create_cart(user_id)
        # проверим, есть ли уже такой товар
        result = await session.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        item = result.scalar_one_or_none()
        if item:
            item.quantity += quantity
        else:
            # фиксируем цену на момент добавления
            price_result = await session.execute(
                select(Product.price).where(Product.id == product_id)
            )
            price = price_result.scalar_one()
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, price_snapshot=price)
            session.add(item)
        await session.commit()
        await session.refresh(item)
        return item


async def get_cart_items(user_id: int):
    """Содержимое корзины"""
    async with AsyncSessionLocal() as session:
        cart = await get_or_create_cart(user_id)
        result = await session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.cart_id == cart.id)
        )
        return result.scalars().all()


async def update_cart_item(cart_item_id: int, quantity: int):
    """Изменение количества товара в корзине"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id == cart_item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
        if quantity <= 0:
            await session.delete(item)
        else:
            item.quantity = quantity
        await session.commit()
        return item


async def remove_cart_item(cart_item_id: int):
    """Удаление позиции из корзины и возврат удалённого объекта"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id == cart_item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None

        await session.delete(item)
        await session.commit()
        return item



async def get_cart_total(user_id: int) -> int:
    """Подсчёт общей стоимости корзины"""
    async with AsyncSessionLocal() as session:
        cart = await get_or_create_cart(user_id)
        result = await session.execute(
            select(func.sum(CartItem.quantity * CartItem.price_snapshot)).where(CartItem.cart_id == cart.id)
        )
        return result.scalar() or 0
