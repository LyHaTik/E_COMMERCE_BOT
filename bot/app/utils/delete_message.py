from aiogram.fsm.context import FSMContext
import logging
from pydantic import ValidationError
from aiogram.exceptions import TelegramBadRequest

from auth import bot


async def deleter(user_id: int, state: FSMContext):
    data = await state.get_data()
    list_message_id = []
    print(data)
    
    product_details_message_dict = data.get("product_details_message_dict", None)
    if product_details_message_dict:
        for product_details_message_id in product_details_message_dict.values():
            list_message_id.append(product_details_message_id)
    
    add_product_message_id = data.get("add_product_message_id", None)
    if add_product_message_id:
        list_message_id.append(add_product_message_id)
        
    message_product_id = data.get("message_product_id", None)
    if message_product_id:
        list_message_id.append(message_product_id)
    
    order_page_message_id = data.get("order_page_message_id", None)
    if order_page_message_id:
        list_message_id.append(order_page_message_id)
    catalog_message_id = data.get("catalog_message_id", None)
    if catalog_message_id:
        list_message_id.append(catalog_message_id)
    start_message_id = data.get("start_message_id", None)
    if start_message_id:
        list_message_id.append(start_message_id)
    cart_item_message_dict = data.get("cart_item_message_dict", None)
    if cart_item_message_dict:
        for cart_item_message_id in cart_item_message_dict.values():
            list_message_id.append(cart_item_message_id)
        
    total_sum_message_id = data.get("total_sum_message_id", None)
    if total_sum_message_id:
        list_message_id.append(total_sum_message_id)
    order_message_dict = data.get("order_message_dict", None)
    if order_message_dict:
        for order_message_id in order_message_dict.values():
            list_message_id.append(order_message_id)
    message_total_sum_order = data.get("message_total_sum_order", None)
    if message_total_sum_order:
        list_message_id.append(message_total_sum_order)
    for message_id in list_message_id:
        try:
            await bot.delete_message(chat_id=user_id, message_id=message_id)
        except ValidationError as e:
            logging.error(f"ValidationError при удалении: {e}")
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest при удалении: {e}")
    
    await state.clear()
