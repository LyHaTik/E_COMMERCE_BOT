from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from pages.start import start_page
from auth import bot
from utils.delete_message import deleter


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await start_page(user_id, state)
    
    
    # Роутер принимающий команды подсказки


@router.message(F.text.in_(("Назад", "Рестарт")))
async def message_back(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await deleter(user_id, state)

    await start_page(user_id, state)


@router.callback_query(F.data.startswith("back_start:"))
async def back_start(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    
    await deleter(user_id, state)
    
    await start_page(user_id, state)