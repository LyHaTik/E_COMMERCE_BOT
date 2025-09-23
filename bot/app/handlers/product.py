from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from db.func.product import put_product, get_or_create_category, edit_product
from pages.start import start_page
from pages.product import (
    add_product_title_page,
    add_product_category_page,
    add_product_description_page,
    add_product_price_page,
    add_product_stock_page,
    add_product_img_page,
    add_product_page,
    add_product_error_64_page,
    add_product_error_validation_page
)
from notifications.product import notifity_add_product, notifity_error, notifity_edit_product
from states.product import ProductStates
from utils.delete_message import cleaner_command, cleaner_message


router = Router()

@router.message(F.text == "Добавить товар")
async def hand_add_product(message: Message, state: FSMContext):
    """
    Обработчик команды "Добавить товар".
    Очищает сообщения, показывает выбор категории и переводит состояние
    в ожидание ввода категории.
    """
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    await cleaner_message(user_id, state)
    
    await add_product_category_page(user_id, state)

    await state.set_state(ProductStates.waiting_for_category_name)


@router.callback_query(F.data.startswith("edit_product:"))
async def hand_edit_product(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик редактирования товара.
    Получает ID товара, очищает сообщения и переводит состояние
    в ожидание ввода категории для редактирования.
    """
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    
    await cleaner_message(user_id, state)
    
    await add_product_category_page(user_id, state)
    
    await state.update_data(product_id=product_id)
    await state.set_state(ProductStates.waiting_for_category_name)

  
async def proceed_category(user_id: int, category: str, state: FSMContext):
    """
    Вспомогательная функция обработки категории.
    Проверяет длину, сохраняет категорию и переводит состояние
    к вводу названия товара.
    """
    if len(category) > 64:
        await add_product_error_64_page(user_id, state)
        logging.error(f"Некорректный ввод product_title от {user_id}: {category!r}")
        return
    await state.update_data(product_category=category)
    await add_product_title_page(user_id, state)
    await state.set_state(ProductStates.waiting_for_product_title)


@router.message(ProductStates.waiting_for_category_name)
async def hand_add_category(message: Message, state: FSMContext):
    """
    Обработчик ввода категории через текстовое сообщение.
    """
    await cleaner_command(message)
    await proceed_category(message.from_user.id, message.text.strip(), state)


@router.callback_query(ProductStates.waiting_for_category_name)
async def hand_edit_category_from_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора категории через callback-кнопку.
    """
    await proceed_category(callback.from_user.id, callback.data, state)

    
@router.message(ProductStates.waiting_for_product_title)
async def hand_add_title(message: Message, state: FSMContext):
    """
    Обработчик ввода названия товара.
    Проверяет длину строки, сохраняет и переводит к вводу описания.
    """
    user_id = int(message.from_user.id)
    product_title = message.text.strip()
    
    await cleaner_command(message)
    
    if len(product_title) > 64:
        await add_product_error_64_page(user_id, state)
        logging.error(f"Некорректный ввод product_title от {user_id}: {message.text!r}")
        return
    
    await state.update_data(product_title=product_title)
    
    await add_product_description_page(user_id, state)
    
    await state.set_state(ProductStates.waiting_for_description)
    

@router.message(ProductStates.waiting_for_description)
async def hand_add_description(message: Message, state: FSMContext):
    """
    Обработчик ввода описания товара.
    Сохраняет описание и переводит к вводу цены.
    """
    user_id = int(message.from_user.id)
    product_description = message.text.strip()
    await cleaner_command(message)
    
    await state.update_data(product_description=product_description)
    
    await add_product_price_page(user_id, state)
    
    await state.set_state(ProductStates.waiting_for_price)


@router.message(ProductStates.waiting_for_price)
async def hand_add_price(message: Message, state: FSMContext):
    """
    Обработчик ввода цены товара.
    Проверяет корректность (число), сохраняет и переводит к вводу количества.
    """
    user_id = int(message.from_user.id)
    await cleaner_command(message)
    
    try:
        product_price = int(message.text.strip())
    except ValueError:
        await add_product_error_validation_page(user_id, state)
        logging.error(f"Некорректный ввод price от {user_id}: {message.text!r}")
        return
    
    await state.update_data(product_price=product_price)
    
    await add_product_stock_page(user_id, state)
    
    await state.set_state(ProductStates.waiting_for_stock)


@router.message(ProductStates.waiting_for_currency)
async def hand_add_currency(message: Message, state: FSMContext):
    """
    Обработчик выбора валюты текстом.
    """
    pass


@router.callback_query(ProductStates.waiting_for_currency)
async def hand_add_currency_from_callback(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора валюты через callback-кнопку.
    """
    pass


@router.message(ProductStates.waiting_for_stock)
async def hand_add_stock_from_text(message: Message, state: FSMContext):
    """
    Обработчик ввода количества товара.
    Проверяет корректность (число), сохраняет и переводит к загрузке фото.
    """
    user_id = int(message.from_user.id)
    await cleaner_command(message)
    
    try:
        product_stock = int(message.text.strip())
    except ValueError:
        await add_product_error_validation_page(user_id, state)
        logging.error(f"Некорректный ввод stock от {user_id}: {message.text!r}")
        return
    
    await state.update_data(product_stock=product_stock)
    
    await add_product_img_page(user_id, state)
    
    await state.set_state(ProductStates.waiting_for_img)


@router.callback_query(ProductStates.waiting_for_stock)
async def hand_add_stock_from_callback(callback: CallbackQuery, state: FSMContext):
    """
    (Заглушка) Обработчик выбора количества через callback-кнопку.
    """
    pass


@router.message(ProductStates.waiting_for_img, F.photo)
async def hand_add_img(message: Message, state: FSMContext):
    """
    Обработчик загрузки фото товара.
    Сохраняет фото и выводит предпросмотр товара.
    """
    img_id = message.photo[-1].file_id 
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    
    await state.update_data(product_img=img_id)
    
    data = await state.get_data()
    product_category = data.get("product_category")
    category = await get_or_create_category(product_category)
    product_title = data.get("product_title")
    product_description = data.get("product_description")
    product_price = data.get("product_price")
    product_stock = data.get("product_stock")
    
    await add_product_page(user_id, category.title, product_title, product_description, product_price, product_stock, img_id, state)
    await state.set_state(None) 


@router.callback_query(F.data.startswith("confirm_product:"))
async def hand_confirm_product(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик подтверждения товара.
    В зависимости от того, редактирование это или новый товар —
    обновляет запись или создает новую в БД, отправляет уведомление
    и возвращает на стартовую страницу.
    """
    user_id = int(callback.from_user.id)
    data = await state.get_data()
    
    product_id = data.get("product_id", None)
    product_category = data.get("product_category")
    category = await get_or_create_category(product_category)
    product_title = data.get("product_title")
    product_description = data.get("product_description")
    product_price = data.get("product_price")
    product_stock = data.get("product_stock")
    product_stock = data.get("product_stock")
    product_img = data.get("product_img")
    
    if product_id:
        product = await edit_product(
            id=product_id,
            category_id=category.id,
            title=product_title,
            description=product_description,
            price=product_price,
            currency=product_stock,
            img_url=product_img
            )
        if product:
            await notifity_edit_product(product.stock, callback)
        else:
            await notifity_error(callback)
            return
    else:
        product = await put_product(
            category.id,
            product_title,
            product_description,
            product_price,
            product_stock,
            product_img
            )
        if product:
            await notifity_add_product(product.stock, callback)
        else:
            await notifity_error(callback)
            return
    await start_page(user_id, state)
