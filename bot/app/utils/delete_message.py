import logging
from pydantic import ValidationError
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from auth import bot


async def cleaner_message(user_id: int, state: FSMContext):
    """Удаляет все сохранённые сообщения пользователя и очищает состояние"""
    data = await state.get_data()
    list_message_id = []

    single_keys = [
        "add_product_message_id",
        "message_product_id",
        "order_page_message_id",
        "catalog_message_id",
        "start_message_id",
        "total_sum_message_id",
        "message_total_sum_order",
        "message_no_order"
    ]

    dict_keys = [
        "product_details_message_dict",
        "cart_item_message_dict",
        "order_message_dict",
    ]

    for key in single_keys:
        message_id = data.get(key)
        if message_id:
            list_message_id.append(message_id)

    for key in dict_keys:
        message_dict = data.get(key)
        if message_dict:
            list_message_id.extend(message_dict.values())

    for message_id in list_message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
        except ValidationError as e:
            logging.error(f"ValidationError при удалении {message_id}: {e}")
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest при удалении {message_id}: {e}")

    await state.clear()


async def cleaner_command(message: Message):
    """Удаляет message-команды"""
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def cleaner_custom(user_id: int, message_id: int):
    """Удаляет message-команды"""
    await bot.delete_message(chat_id=user_id, message_id=message_id)
    