from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from states.product import AddProduct
from utils.delete_message import deleter
from auth import bot
from db.func.product import put_product, get_or_create_category, edit_product
from notifications.product import notifity_add_product, notifity_error, notifity_edit_product
from pages.start import start_page
from pages.product import (
    add_product_title_page,
    add_product_category_page,
    add_product_description_page,
    add_product_price_page,
    add_product_stock_page,
    add_product_img_page,
    add_product_page
)


router = Router()


@router.message(F.text == "Добавить товар")
async def hand_add_product(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await deleter(user_id, state)
    
    await add_product_category_page(user_id, state)

    await state.set_state(AddProduct.waiting_for_category_name)


#########################################################################################    
@router.message(AddProduct.waiting_for_category_name)
async def hand_add_category(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    product_category = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(product_category=product_category)
    
    await add_product_title_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_product_title)


@router.callback_query(AddProduct.waiting_for_category_name)
async def hand_edit_category_from_callback(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    product_category = callback.data
    
    await state.update_data(product_category=product_category)
    
    await add_product_title_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_product_title)
    
    
#########################################################################################
@router.message(AddProduct.waiting_for_product_title)
async def hand_add_title(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    product_title = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(product_title=product_title)
    
    await add_product_description_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_description)
    

#########################################################################################
@router.message(AddProduct.waiting_for_description)
async def hand_add_description(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    product_description = message.text
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
    await state.update_data(product_description=product_description)
    
    await add_product_price_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_price)

#########################################################################################
@router.message(AddProduct.waiting_for_price)
async def hand_add_price(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    try:
        product_price = int(message.text)
    except:
        # Сообщение ошибки
        logging.error()
        return
    
    await state.update_data(product_price=product_price)
    
    await add_product_stock_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_stock)

#########################################################################################
@router.message(AddProduct.waiting_for_currency)
async def hand_add_currency(message: Message, state: FSMContext):
    pass


@router.callback_query(AddProduct.waiting_for_currency)
async def hand_add_currency_from_callback(callback: CallbackQuery, state: FSMContext):
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_stock)
async def hand_add_stock_from_text(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    try:
        product_stock = int(message.text)
    except:
        # notifity error stock
        logging.error()
        return
    
    await state.update_data(product_stock=product_stock)
    
    await add_product_img_page(user_id, state)
    
    await state.set_state(AddProduct.waiting_for_img)


@router.callback_query(AddProduct.waiting_for_stock)
async def hand_add_stock_from_callback(callback: CallbackQuery, state: FSMContext):
    # state.data = stock
    # Соббщение Отправте фото
    # state AddProduct waiting_for_img
    pass

#########################################################################################
@router.message(AddProduct.waiting_for_img)
@router.message(F.photo)
async def hand_add_img(message: Message, state: FSMContext):
    img_id = message.photo[-1].file_id 
    user_id = int(message.from_user.id)
    
    await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    
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
async def hand_add_stock_from_callback(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    data = await state.get_data()
    
    product_id = data.get("product_category", None)
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
            await notifity_edit_product(product, callback)
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
            await notifity_add_product(product, callback)
        else:
            await notifity_error(callback)
            return
    await start_page(user_id, state)
