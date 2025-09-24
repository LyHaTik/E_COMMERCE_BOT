from aiogram.utils.keyboard import InlineKeyboardBuilder

from shared.db.models import OrderStatus, Order, DeliveryMethod


def order_confirm_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Подвердить', callback_data=f"confirm_order:")
    kb.button(text=f'Отмена', callback_data=f"back_start:")
    kb.adjust(2)
    return kb.as_markup()


def order_status_ikb(order: Order):
    kb = InlineKeyboardBuilder()
    for status in OrderStatus:
        if not order.status == status.value:
            kb.button(text=status.value, callback_data=f"edit_order_status:{status.value}:{order.id}")
    kb.adjust(4)
    return kb.as_markup()


def order_delivery_method_ikb():
    kb = InlineKeyboardBuilder()
    for delivery_method in DeliveryMethod:
        kb.button(text=delivery_method.value, callback_data=delivery_method.value)
    kb.adjust(2)
    return kb.as_markup()