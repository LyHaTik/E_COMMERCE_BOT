"""add_to_cart(product_id, quantity) — добавить товар

show_cart() — список товаров в корзине + кнопки редактирования/удаления

update_cart_item(cart_item_id, quantity) — изменить количество

remove_cart_item(cart_item_id) — удалить"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.cart import CartStates
from pages.cart import cart_page, edit_cart_page
from db.func.cart import get_cart_item, update_cart_item, remove_cart_item
from auth import bot
from utils.delete_message import deleter
from notifications.cart import notifity_error_count


router = Router()

# отображаем содержимое корзины
@router.message(F.text == "Корзина")
async def hand_categories(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await deleter(user_id, state)
    
    await cart_page(user_id, state)


@router.callback_query(F.data.startswith("minus:"))
async def hand_minus_product(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, cart_item_id = callback.data.split(":")
    
    cart_item = await get_cart_item(int(cart_item_id))
    quantity = cart_item.quantity - 1
    cart_item = await update_cart_item(cart_item.id, quantity)
    status_delete = None
    if quantity == 0:
        status_delete = True
    
    await edit_cart_page(user_id, cart_item, state, status_delete)


@router.callback_query(F.data.startswith("plus:"))
async def hand_plus_product(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, cart_item_id = callback.data.split(":")
    
    cart_item = await get_cart_item(int(cart_item_id))
    
    quantity = cart_item.quantity + 1
    if quantity > cart_item.product.stock:
        await notifity_error_count(cart_item, callback)
        return
    cart_item = await update_cart_item(cart_item.id, quantity)
    
    await edit_cart_page(user_id, cart_item, state)


@router.callback_query(F.data.startswith("delete:"))
async def hand_plus_product(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, cart_item_id = callback.data.split(":")
    
    cart_item = await remove_cart_item(int(cart_item_id))
    
    await edit_cart_page(user_id, cart_item, state, status_delete=True)