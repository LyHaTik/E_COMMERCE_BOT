"""FSM для оформления заказа

Сбор данных пользователя (name, phone, address)

Выбор метода доставки

Подтверждение заказа + генерация номера

Сохранение в таблицу Order и OrderItem"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.states.order import OrderStates
from app.states.contact import ContactStates


router = Router()

# отображаем список заказов
@router.message(F.text == "Список заказов")
async def hand_order_list(message: Message):
    # Каждое сообщение Заказ с инлайн кнопкой Изменить статус
    # state waiting_for_edit_status_order
    pass


@router.callback_query(OrderStates.waiting_for_edit_status_order)
async def hand_edit_status_order(callback: CallbackQuery):
    _, order_id = callback.data.split(":")
    # state.data = order_id
    # Сообщение с списком статусов в инлайн кнопках
    pass


@router.callback_query(OrderStates.waiting_for_edit_status_order)
async def hand_edit_status_order(callback: CallbackQuery):
    # Изменяем статус в БД
    # Каждое сообщение Заказ с инлайн кнопкой Изменить статус
    # state waiting_for_edit_status_order
    pass