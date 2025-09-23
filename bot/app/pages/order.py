from aiogram.fsm.context import FSMContext

from auth import bot
from keyboards.order_kb import order_confirm_ikb, order_status_ikb
from keyboards.start_kb import back_kb, main_kb
from db.func.cart import get_cart_items, get_cart_total
from db.func.order import get_list_order
from db.func.user import get_or_create_user
from db.models import Order



async def order_page(user_id: int, state: FSMContext):
    total_sum = await get_cart_total(user_id)
    cart = await get_cart_items(user_id)
    
    data = await state.get_data()
    order_page_message_id = data.get("order_page_message_id")
    
    text=f"Ваш заказ:\n"
    for cart_item in cart:
        text += f"{cart_item.product.title} {cart_item.quantity}шт. {cart_item.quantity*cart_item.price_snapshot}\n"
    text += f'Сумма: {total_sum}'
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_page_message_id,
        text=text,
        reply_markup=order_confirm_ikb()
    )


async def create_order_page(user_id: int, order: Order):
    user = await get_or_create_user(user_id)
    
    await bot.send_message(
        chat_id=user_id,
        text=f'Заказ №{order.order_number} оформлен.',
        reply_markup=main_kb(user.is_admin)
    )


async def list_order_page(user_id: int, state: FSMContext):
    orders_not_completed = await get_list_order()
    
    order_message_dict = {}
    
    if not orders_not_completed:
        message_no_order = await bot.send_message(
            chat_id=user_id,
            text="Нет активных заказов",
            reply_markup=back_kb())
        await state.update_data(message_no_order=message_no_order.message_id)
        return
    
    total_sum_order = 0
    for order in orders_not_completed:
        message_order = await bot.send_message(
            chat_id=user_id,
            text=(
                f"№ {order.order_number}\n"
                f"status: {order.status}\n"
                f"сумма: {order.total}"
                ),
            reply_markup=order_status_ikb(order)
        )
        order_message_dict[order.id] = message_order.message_id
        total_sum_order += order.total

    await state.update_data(order_message_dict=order_message_dict)
    
    message_total_sum_order = await bot.send_message(
        chat_id=user_id,
        text=f"Сумма: {total_sum_order}",
        reply_markup=back_kb()
        )
    
    await state.update_data(message_total_sum_order=message_total_sum_order.message_id)


async def edit_list_order_page(user_id: int, order: Order, state: FSMContext):
    data = await state.get_data()
    order_message_dict = data.get("order_message_dict")
    order_message_id = order_message_dict[order.id]
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=order_message_id,
        text=f"№ {order.order_number}\n"
             f"status: {order.status}\n"
             f"сумма: {order.total}",
        reply_markup=order_status_ikb(order)
        )


async def send_client_edit_status(order: Order):
    
    await bot.send_message(
        chat_id=order.user_id,
        text=f"Изменился статус заказа №{order.order_number}: {order.status}"
        )