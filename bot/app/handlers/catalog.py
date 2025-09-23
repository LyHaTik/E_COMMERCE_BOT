from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from db.func.cart import add_to_cart
from pages.catalog import categories_page, product_list_page, product_details_page, edit_categories_page
from notifications.catalog import notifity_to_cart, notifity_error, notifity_tap
from utils.delete_message import cleaner_command, cleaner_message, cleaner_custom


router = Router()


@router.message(F.text == "Каталог товаров")
async def hand_categories(message: Message, state: FSMContext):
    """Показывает страницу категорий товаров пользователю."""
    user_id = int(message.from_user.id)
    
    await cleaner_command(message)
    await cleaner_message(user_id, state)
    
    await categories_page(user_id, state)
    
    logging.info(f"Выбор товара, user: {user_id}")
        

@router.callback_query(F.data.startswith("product_list:"))
async def hand_product_list(callback: CallbackQuery, state: FSMContext):
    """Показывает список товаров выбранной категории."""
    user_id = int(callback.from_user.id)
    _, category_id = callback.data.split(":")
    
    await product_list_page(user_id, int(category_id), state)

    

@router.callback_query(F.data.startswith("product_details:"))
async def hand_product_details(callback: CallbackQuery, state: FSMContext):
    """Показывает детали выбранного товара."""
    user_id = int(callback.from_user.id)
    command, product_id = callback.data.split(":")
    
    await notifity_tap(command, callback)
    await product_details_page(user_id, int(product_id), state)
    

@router.callback_query(F.data.startswith("to_cart:"))
async def hand_product_to_cart(callback: CallbackQuery, state: FSMContext):
    """Добавляет товар в корзину пользователя."""
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    
    item = await add_to_cart(user_id, int(product_id))
    if item:
        await notifity_to_cart(item.quantity, callback)
    else:
        await notifity_error(callback)


@router.callback_query(F.data.startswith("back_product_list:"))
async def hand_back_product_list(callback: CallbackQuery, state: FSMContext):
    """Возврат к списку товаров категории, удаляя сообщение с деталями."""
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    
    data = await state.get_data()
    product_details_message_dict = data.get("product_details_message_dict")
    product_message_id = product_details_message_dict[int(product_id)]
    
    await cleaner_custom(user_id, product_message_id)


@router.callback_query(F.data.startswith("back_categories:"))
async def hand_back_categories(callback: CallbackQuery, state: FSMContext):
    """Возврат к странице категорий товаров."""
    user_id = int(callback.from_user.id)
    
    await edit_categories_page(user_id, state)
