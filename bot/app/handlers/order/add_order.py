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

    
@router.callback_query(F.data.startswith("order_add:"))
async def hand_order(callback: CallbackQuery):
    _, cart_id = callback.data.split(":")
    # достает данные пользователя и выводит в сообщение с inline кнопками "Подвердить контакты" и "Изменить контакты?"
    # Если "Подвердить", сообщение с выбором метода доставки
    # Если "Изменить", устанавливаем состояние waiting_for_name
    # Сбор данных пользователя (name, phone, address)
    
    
@router.callback_query(ContactStates.waiting_for_name)
async def hand_waiting_for_name(callback: CallbackQuery):
    pass
    # Сохраняем name в state.data
    # устанавливаем состояние waiting_for_phone


@router.callback_query(ContactStates.waiting_for_phone)
async def hand_waiting_for_phone(callback: CallbackQuery):
    # Сохраняем phone в state.data
    # устанавливаем состояние waiting_for_address
    pass


@router.callback_query(ContactStates.waiting_for_address)
async def hand_waiting_for_address(callback: CallbackQuery):
    # Сохраняем address в state.data
    # устанавливаем состояние waiting_for_delivery_method
    # собщение с выбором метода доставки в ин-лайн кнопках.
    pass


@router.callback_query(ContactStates.waiting_for_delivery_method)
async def hand_waiting_for_delivery_method(callback: CallbackQuery):
    # собщение с выбором Подтвердить Заказ, "Удалить Заказ"
    # устанавливаем state.OrderState
    pass


@router.callback_query(ContactStates.waiting_for_delivery_method)
async def hand_waiting_for_delivery_method(callback: CallbackQuery):
    # сохраняем заказ
    # собщение с выбором об успешном создании и номером заказа и c кнопкой старт
    # очистка state и state.data
    # 
    pass
