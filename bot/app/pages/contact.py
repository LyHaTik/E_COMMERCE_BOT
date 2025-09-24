from aiogram.fsm.context import FSMContext

from auth import bot
from shared.db.func.user import get_or_create_user
from keyboards.contact_kb import contact_confirm_ikb
from keyboards.order_kb import order_delivery_method_ikb


async def contact_page(user_id: int, state: FSMContext):
    user = await get_or_create_user(user_id)
    user_name = user.name if user.name else ""
    user_phone = user.phone if user.phone else ""
    user_address = user.address if user.address else ""
    
    message = await bot.send_message(
        chat_id=user_id,
        text=f"Заполните контактную информацию:\n\
            Имя: {user_name}\n\
            Телефон: {user_phone}\n\
            Адрес: {user_address}",
        reply_markup=contact_confirm_ikb()
        )
    
    await state.update_data(order_page_message_id=message.message_id)


async def delivery_method_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    order_page_message_id = data.get("order_page_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_page_message_id,
        text=f"Выберите метод доставки:",
        reply_markup=order_delivery_method_ikb()
    )


async def send_name(user_id: int, state: FSMContext):
    data = await state.get_data()
    order_page_message_id = data.get("order_page_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_page_message_id,
        text=f"Введите имя:"
    )


async def send_phone(user_id: int, state: FSMContext):
    data = await state.get_data()
    order_page_message_id = data.get("order_page_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_page_message_id,
        text=f"Введите телефон:"
    )
    
    
async def send_address(user_id: int, state: FSMContext):
    data = await state.get_data()
    order_page_message_id = data.get("order_page_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_page_message_id,
        text=f"Введите адрес:"
    )