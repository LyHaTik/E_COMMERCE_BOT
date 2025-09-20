from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.db.func.user import get_or_create_user

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = int(message.from_user.id)
    user_name = message.from_user.full_name
    user = await get_or_create_user(user_id, user_name)
    # 
    # Если админ добавить кнопки Списка заказов и Добавление товара
    # Добавить названия продкутов в подсказки сформировав команды
    await send_main_menu(message, user)
    
    
    # Роутер принимающий команды подсказки