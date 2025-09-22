"""FSM для оформления заказа

Сбор данных пользователя (name, phone, address)

Выбор метода доставки

Подтверждение заказа + генерация номера

Сохранение в таблицу Order и OrderItem"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.order import OrderStates
from states.contact import ContactStates
from auth import bot
from db.func.user import put_user_contact, get_or_create_user
from db.func.order import create_order
from pages.contact import contact_page, delivery_method_page, send_name, send_phone, send_address
from pages.order import order_page, create_order_page
from utils.delete_message import deleter


router = Router()

    
@router.callback_query(F.data.startswith("add_order"))
async def hand_order(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    
    await deleter(user_id, state)
    
    await contact_page(user_id, state)

    
@router.callback_query(F.data.startswith("confirm_contact:"))
async def hand_confirm_contact(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)

    await delivery_method_page(user_id, state)
    await state.set_state(ContactStates.waiting_for_delivery_method)


@router.callback_query(F.data.startswith("edit_contact:"))
async def hand_edit_contact(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    
    await send_name(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_name)
    
    
@router.message(ContactStates.waiting_for_name)
async def hand_waiting_for_name(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    name = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(contact_name=name)
    
    await send_phone(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_phone)


@router.message(ContactStates.waiting_for_phone)
async def hand_waiting_for_phone(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    phone = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(contact_phone=phone)
    
    await send_address(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_address)


@router.message(ContactStates.waiting_for_address)
async def hand_waiting_for_address(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    address = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(contact_address=address)
    
    await delivery_method_page(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_delivery_method)


@router.callback_query(ContactStates.waiting_for_delivery_method)
async def hand_waiting_for_delivery_method(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    delivery_method = callback.data
    
    await state.update_data(delivery_method=delivery_method)
    
    await order_page(user_id, state)
    
    await state.set_state()


@router.callback_query(F.data.startswith("confirm_order:"))
async def hand_confirm_order(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    message_id = callback.message.message_id
    await bot.delete_message(chat_id=user_id, message_id=message_id)

    data = await state.get_data()
    contact_name = data.get("contact_name")
    contact_phone = data.get("contact_phone")
    contact_address = data.get("contact_address")
    delivery_method = data.get("delivery_method")

    if contact_name and contact_phone and contact_address:
        user = await put_user_contact(user_id, contact_name, contact_phone, contact_address)
    else:
        user = await get_or_create_user(user_id)
    order = await create_order(
        user.id,
        user.name,
        user.phone,
        user.address,
        delivery_method
        )
    
    await create_order_page(user_id, order)

