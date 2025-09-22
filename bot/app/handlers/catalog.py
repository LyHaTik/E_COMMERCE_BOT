"""
/start — приветствие + кнопка «Каталог товаров»

show_categories() — inline-кнопки категорий

show_products(category_id) — товары выбранной категории

show_product_detail(product_id) — фото, описание, цена, кнопка «В корзину»"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from pages.catalog import categories_page, product_list_page, product_details_page, edit_categories_page
from db.func.cart import add_to_cart
from pages.start import start_page
from auth import bot
from notifications.catalog import notifity_to_cart, notifity_error
from utils.delete_message import deleter


router = Router()


# отображаем список категорий
@router.message(F.text == "Каталог товаров")
async def hand_categories(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)

    await deleter(user_id, state)
    
    await categories_page(user_id, state)
        

# отображаем товары
@router.callback_query(F.data.startswith("product_list:"))
async def hand_product_list(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, category_id = callback.data.split(":")
    await product_list_page(user_id, int(category_id), state)

    
# детальная информация о товаре
@router.callback_query(F.data.startswith("product_details:"))
async def hand_product_details(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    await product_details_page(user_id, int(product_id), state)
    

@router.callback_query(F.data.startswith("to_cart:"))
async def hand_product_to_cart(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    item = await add_to_cart(user_id, int(product_id))
    if item:
        await notifity_to_cart(item, callback)
    else:
        await notifity_error(callback)


@router.callback_query(F.data.startswith("back_product_list:"))
async def back_product_list(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    _, product_id = callback.data.split(":")
    
    data = await state.get_data()
    product_details_message_dict = data.get("product_details_message_dict")
    product_message_id = product_details_message_dict[int(product_id)]
    
    await bot.delete_message(chat_id=user_id, message_id=product_message_id)


@router.callback_query(F.data.startswith("back_categories:"))
async def back_categories(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    
    data = await state.get_data()
    catalog_message_id = data.get("catalog_message_id")
    
    await edit_categories_page(user_id, catalog_message_id)
