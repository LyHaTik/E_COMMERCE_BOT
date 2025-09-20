"""/admin — проверка прав

add_product() — шаги для добавления товара (FSM можно)

edit_product() — редактирование

delete_product() — удаление

show_orders() — список заказов

update_order_status() — изменение статуса"""
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.product import EditProduct


router = Router()


@router.callback_query(F.data.startswith("edit_product:"))
async def hand_edit_product(callback: CallbackQuery):
    _, product_id = callback.data.split(":")
    # state.data = product_id
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock

#######################################################################################
@router.callback_query(F.data.startswith("edit_product_title"))
async def hand_edit_product_title(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите новое название продукта
    # state  EditProduct.waiting_for_product_title
    pass


@router.message(EditProduct.waiting_for_product_title)
async def hand_edit_title_from_message(message: Message, state: FSMContext):
    # сохраняем title в БД
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass


@router.message(EditProduct.waiting_for_product_title)
async def hand_edit_title_from_callback(callback: CallbackQuery, state: FSMContext):
    # сохраняем title в БД
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

################################################################################################
@router.callback_query(F.data.startswith("edit_product_category"))
async def hand_edit_product_category(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите новое название категории или выбери из предолженных в инлайн кнопках
    # state  EditProduct.waiting_for_product_category
    pass

    
@router.message(EditProduct.waiting_for_category_name)
async def hand_edit_category_from_text(message: Message, state: FSMContext):
    # сохраняем category в БД
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass


@router.callback_query(EditProduct.waiting_for_category_name)
async def hand_edit_category_from_callback(callback: CallbackQuery, state: FSMContext):
    # сохраняем category в БД
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

############################################################################################################
@router.callback_query(F.data.startswith("edit_product_description"))
async def hand_edit_product_description(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите описание
    # state  EditProduct.waiting_for_product_description
    pass


@router.message(EditProduct.waiting_for_description)
async def hand_edit_description_from_text(message: Message, state: FSMContext):
    # сохраняем описание в БД
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

########################################################################################################
@router.callback_query(F.data.startswith("edit_product_price"))
async def hand_edit_product_price(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите стоимость
    # state  EditProduct.waiting_for_product_price
    pass


@router.message(EditProduct.waiting_for_price)
async def hand_edit_price_from_text(message: Message, state: FSMContext):
    # сохраняем стоимость
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

########################################################################################################
@router.callback_query(F.data.startswith("edit_product_currency"))
async def hand_edit_product_currency(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите валюту и инлайн кнопки с сущестующей валютой
    # state  EditProduct.waiting_for_product_currency
    pass


@router.message(EditProduct.waiting_for_currency)
async def hand_edit_currency_from_text(message: Message, state: FSMContext):
    # сохраняем валюту
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass


@router.callback_query(EditProduct.waiting_for_currency)
async def hand_edit_currency_from_callback(callback: CallbackQuery, state: FSMContext):
    # сохраняем валюту
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

############################################################################################################
@router.callback_query(F.data.startswith("edit_product_stock"))
async def hand_edit_product_stock(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите валюту и инлайн кнопки с сущестующей валютой
    # state  EditProduct.waiting_for_product_stock
    pass


@router.message(EditProduct.waiting_for_stock)
async def hand_edit_stock_from_tex(message: Message, state: FSMContext):
    # сохраняем кол-во
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass


@router.callback_query(EditProduct.waiting_for_stock)
async def hand_edit_stock_from_callback(callback: CallbackQuery, state: FSMContext):
    # сохраняем кол-во
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass

######################################################################################################
@router.callback_query(F.data.startswith("edit_product_img"))
async def hand_edit_product_img(callback: CallbackQuery, state: FSMContext):
    # Сообщение Напишите валюту и инлайн кнопки с сущестующей валютой
    # state  EditProduct.waiting_for_product_img
    pass


@router.message(EditProduct.waiting_for_img)
async def hand_edit_img(message: Message, state: FSMContext):
    # Сохранение фото
    # Сообщение с инлайн кнопками Title, category, price, currency, description, img, stock
    # очищаем state
    pass
