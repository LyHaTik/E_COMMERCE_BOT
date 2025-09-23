from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from pages.start import start_page
from utils.delete_message import cleaner_command, cleaner_message


router = Router()

@router.message(Command("start"))
async def hand_cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start.
    Очищает исходное сообщение и показывает стартовую страницу.
    """
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    
    await start_page(user_id, state)
    
    
    # Роутер принимающий команды подсказки


@router.message(F.text == "Назад")
async def hand_message_back(message: Message, state: FSMContext):
    """
    Обработчик кнопки "Назад".
    Очищает сообщение и состояние пользователя, затем возвращает на стартовую страницу.
    """
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    await cleaner_message(user_id, state)

    await start_page(user_id, state)


@router.callback_query(F.data.startswith("back_start:"))
async def hand_call_back_start(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик callback-кнопки возврата на стартовую страницу.
    Очищает сообщения пользователя и выводит стартовую страницу.
    """
    user_id = int(callback.from_user.id)
    
    await cleaner_message(user_id, state)
    
    await start_page(user_id, state)