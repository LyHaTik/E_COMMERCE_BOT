from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from pages.order import list_order_page, edit_list_order_page, send_client_edit_status
from db.func.user import get_or_create_user
from db.func.order import update_order_status
from pages.start import start_page
from auth import bot
from notifications.catalog import notifity_to_cart, notifity_error
from utils.delete_message import deleter


router = Router()


# отображаем список категорий
@router.message(F.text == "Заказы")
async def hand_categories(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    user = await get_or_create_user(user_id)
    
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await deleter(user_id, state)
    
    if user.is_admin:
        await list_order_page(user_id, state)
        

@router.callback_query(F.data.startswith("edit_order_status:"))
async def hand_order(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, status, order_id = callback.data.split(":")
    order = await update_order_status(int(order_id), status)
    
    await send_client_edit_status(order)
    await edit_list_order_page(user_id, order, state)