"""add_to_cart(product_id, quantity) — добавить товар

show_cart() — список товаров в корзине + кнопки редактирования/удаления

update_cart_item(cart_item_id, quantity) — изменить количество

remove_cart_item(cart_item_id) — удалить"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.cart import CartStates

router = Router()


# отображаем содержимое корзины
@router.message(F.text == "Корзина")
async def hand_categories(message: Message, state: FSMContext):
    # каждый товар отображается отдельным сообщением
    # отображает название товара
    # inline кнопка уменьшить кол-во
    # inline кнопка кол-во (заглушка, только отображает кол-во)
    # inline кнопка увеличить кол-во
    # inline кнопка удалить товар из корзины
    # последнее сообщение с общей стоимостью и inline кнопкой "Заказать"
    pass


@router.callback_query(F.data.startswith("minus:"))
async def hand_minus_product(callback: CallbackQuery):
    _, product_message_id, total_message_id = callback.data.split(":")
    # изменяет сообщение товара в котором изменили кол-во
    # изменяет сообщение с общей стоимостью


@router.callback_query(F.data.startswith("plus:"))
async def hand_plus_product(callback: CallbackQuery):
    _, product_message_id, total_message_id = callback.data.split(":")
    # изменяет сообщение товара в котором изменили кол-во
    # изменяет сообщение с общей стоимостью


@router.callback_query(F.data.startswith("delete:"))
async def hand_plus_product(callback: CallbackQuery):
    _, product_message_id, total_message_id = callback.data.split(":")
    # удаляет сообщение товара
    # изменяет сообщение с общей стоимостью