from aiogram.fsm.context import FSMContext

from auth import bot
from keyboards.cart_kb import cart_item_ikb, cart_confirm_ikb, cart_back_ikb
from shared.db.func.cart import get_cart_items, get_cart_total
from shared.db.models import CartItem


async def cart_page(user_id: int, state: FSMContext):
    cart_items = await get_cart_items(user_id)
    if cart_items:
        total_sum = await get_cart_total(user_id)
        cart_item_message_dict = {}
        for item in cart_items:
            message_item = await bot.send_message(
                chat_id=user_id,
                text=f"{item.product.title} - {item.price_snapshot*item.quantity} {item.product.currency}",
                reply_markup=cart_item_ikb(item.id, item.quantity)
                )
            cart_item_message_dict[item.id] = message_item.message_id
        await state.update_data(cart_item_message_dict=cart_item_message_dict)
            
        message_total_sum = await bot.send_message(
                chat_id=user_id,
                text=f"Сумма: {total_sum}",
                reply_markup=cart_confirm_ikb()
                )

        await state.update_data(total_sum_message_id=message_total_sum.message_id)
        
    else:
        message_total_sum = await bot.send_message(
                chat_id=user_id,
                text="Корзина пуста",
                reply_markup=cart_back_ikb()
                )
        
        await state.update_data(total_sum_message_id=message_total_sum.message_id)
    
    
async def edit_cart_page(user_id: int, cart_item: CartItem, state: FSMContext, status_delete: bool = False):
    total_sum = await get_cart_total(user_id)
        
    data = await state.get_data()
    total_sum_message_id = data.get("total_sum_message_id")
    cart_item_message_dict = data.get("cart_item_message_dict")
    product_message_id = cart_item_message_dict[cart_item.id]
    
    if status_delete:
        await bot.delete_message(
            chat_id=user_id,
            message_id=product_message_id
        )
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            text=f"{cart_item.product.title} - {cart_item.price_snapshot*cart_item.quantity} {cart_item.product.currency}",
            message_id=product_message_id,
            reply_markup=cart_item_ikb(cart_item.id, cart_item.quantity)
            )
    
    if total_sum == 0:
        await bot.edit_message_text(
                chat_id=user_id,
                message_id=total_sum_message_id,
                text=f"Корзина пуста",
                reply_markup=cart_back_ikb()
                )
        
    else:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=total_sum_message_id,
            text=f"Сумма: {total_sum}",
            reply_markup=cart_confirm_ikb()
            )
