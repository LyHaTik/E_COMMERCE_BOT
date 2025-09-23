from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from db.func.cart import get_cart_item, update_cart_item, remove_cart_item
from pages.cart import cart_page, edit_cart_page
from notifications.cart import notifity_error_count
from utils.delete_message import cleaner_message, cleaner_command


router = Router()


@router.message(F.text == "Корзина")
async def hand_cart(message: Message, state: FSMContext):
    """Показывает страницу корзины пользователю."""
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    await cleaner_message(user_id, state)
    
    await cart_page(user_id, state)
    
    logging.info(f"Действия в корзине, user: {user_id}")


@router.callback_query(F.data.startswith("minus:"))
async def hand_cart_minus_product(callback: CallbackQuery, state: FSMContext):
    """Уменьшает количество товара в корзине. Удаляет товар, если количество стало 0."""
    user_id = callback.from_user.id
    _, cart_item_id = callback.data.split(":")

    cart_item = await get_cart_item(int(cart_item_id))

    quantity = cart_item.quantity - 1
    status_delete = quantity == 0

    cart_item = await update_cart_item(cart_item.id, quantity)

    await edit_cart_page(user_id, cart_item, state, status_delete)


@router.callback_query(F.data.startswith("plus:"))
async def hand_cart_plus_product(callback: CallbackQuery, state: FSMContext):
    """Увеличивает количество товара в корзине. Проверяет доступный сток."""
    user_id = int(callback.from_user.id)
    _, cart_item_id = callback.data.split(":")
    
    cart_item = await get_cart_item(int(cart_item_id))
    
    stock = cart_item.product.stock
    quantity = cart_item.quantity + 1
    if quantity > stock:
        await notifity_error_count(stock, callback)
        return
    
    cart_item = await update_cart_item(cart_item.id, quantity)
    
    await edit_cart_page(user_id, cart_item, state)


@router.callback_query(F.data.startswith("delete:"))
async def hand_cart_delete_product(callback: CallbackQuery, state: FSMContext):
    """Удаляет товар из корзины полностью."""
    user_id = int(callback.from_user.id)
    _, cart_item_id = callback.data.split(":")
    
    cart_item = await remove_cart_item(int(cart_item_id))
    
    await edit_cart_page(user_id, cart_item, state, status_delete=True)