from aiogram.fsm.context import FSMContext

from auth import bot
from db.func.user import get_or_create_user
from keyboards.start_kb import main_kb
from utils.delete_message import cleaner_message


async def start_page(user_id: int, state: FSMContext):
    await cleaner_message(user_id, state)
    
    user = await get_or_create_user(user_id)
    
    message = await bot.send_message(
        chat_id=user_id,
        text="Найдите товар по каталогу или напишите название Продукта",
        reply_markup=main_kb(user.is_admin)
        )
    
    await state.update_data(start_message_id=message.message_id)