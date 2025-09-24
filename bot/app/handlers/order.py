from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from shared.db.func.user import get_or_create_user, put_user_contact
from shared.db.func.order import update_order_status, create_order
from pages.order import list_order_page, edit_list_order_page, send_client_edit_status, order_page, create_order_page
from pages.contact import contact_page, delivery_method_page, send_name, send_phone, send_address
from states.contact import ContactStates
from utils.delete_message import cleaner_command, cleaner_message


router = Router()


@router.message(F.text == "Заказы")
async def hand_orders(message: Message, state: FSMContext):
    """
    Обработчик команды "Заказы".
    Создает или получает пользователя и, если он администратор,
    очищает предыдущие сообщения и показывает список заказов.
    """
    user_id = int(message.from_user.id)
    user = await get_or_create_user(user_id)
    
    await cleaner_command(message)
    await cleaner_message(user_id, state)
    
    if user.is_admin:
        await list_order_page(user_id, state)
        

@router.callback_query(F.data.startswith("edit_order_status:"))
async def hand_edit_order_status(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик изменения статуса заказа.
    Извлекает ID заказа и новый статус, обновляет его в БД,
    уведомляет клиента и обновляет список заказов.
    """
    user_id = int(callback.from_user.id)
    _, status, order_id = callback.data.split(":")
    order = await update_order_status(int(order_id), status)
    
    await send_client_edit_status(order)
    await edit_list_order_page(user_id, order, state)


@router.callback_query(F.data.startswith("add_order"))
async def hand_add_order(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик добавления нового заказа.
    Очищает предыдущие сообщения и открывает форму для ввода контактов.
    """
    user_id = int(callback.from_user.id)
    
    await cleaner_message(user_id, state)
    
    await contact_page(user_id, state)

    
@router.callback_query(F.data.startswith("confirm_contact:"))
async def hand_confirm_contact(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик подтверждения контактных данных.
    Показывает выбор способа доставки и переводит состояние.
    """
    user_id = int(callback.from_user.id)

    await delivery_method_page(user_id, state)
    await state.set_state(ContactStates.waiting_for_delivery_method)


@router.callback_query(F.data.startswith("edit_contact:"))
async def hand_edit_contact(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик редактирования контактных данных.
    Запрашивает у пользователя новое имя и переводит состояние.
    """
    user_id = int(callback.from_user.id)
    
    await send_name(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_name)
    
    
@router.message(ContactStates.waiting_for_name)
async def hand_waiting_for_name(message: Message, state: FSMContext):
    """
    Обработчик ввода имени пользователя.
    Сохраняет имя, очищает сообщение и запрашивает телефон.
    """
    user_id = int(message.from_user.id)
    name = message.text
    await cleaner_command(message)
    
    await state.update_data(contact_name=name)
    
    await send_phone(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_phone)


@router.message(ContactStates.waiting_for_phone)
async def hand_waiting_for_phone(message: Message, state: FSMContext):
    """
    Обработчик ввода телефона пользователя.
    Сохраняет телефон, очищает сообщение и запрашивает адрес.
    """
    user_id = int(message.from_user.id)
    phone = message.text
    await cleaner_command(message)
    
    await state.update_data(contact_phone=phone)
    
    await send_address(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_address)


@router.message(ContactStates.waiting_for_address)
async def hand_waiting_for_address(message: Message, state: FSMContext):
    """
    Обработчик ввода адреса пользователя.
    Сохраняет адрес, очищает сообщение и показывает выбор доставки.
    """
    user_id = int(message.from_user.id)
    address = message.text
    await cleaner_command(message)
    
    await state.update_data(contact_address=address)
    
    await delivery_method_page(user_id, state)
    
    await state.set_state(ContactStates.waiting_for_delivery_method)


@router.callback_query(ContactStates.waiting_for_delivery_method)
async def hand_waiting_for_delivery_method(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора метода доставки.
    Сохраняет способ доставки и показывает страницу заказа.
    """
    user_id = int(callback.from_user.id)
    delivery_method = callback.data
    
    await state.update_data(delivery_method=delivery_method)
    
    await order_page(user_id, state)
    
    await state.set_state()


@router.callback_query(F.data.startswith("confirm_order:"))
async def hand_confirm_order(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик подтверждения заказа.
    Получает контактные данные, сохраняет их в БД,
    создает заказ и показывает страницу подтверждения.
    """
    user_id = int(callback.from_user.id)
    message = callback.message
    await cleaner_command(message)

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
    
    logging.info(f"Заказ подтвержден, user: {user_id}")

