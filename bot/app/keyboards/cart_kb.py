from aiogram.utils.keyboard import InlineKeyboardBuilder


def cart_item_ikb(item_id: int, item_quantity: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='-', callback_data=f"minus:{item_id}")
    kb.button(text=f'{item_quantity}', callback_data=f"заглушка")
    kb.button(text='+', callback_data=f"plus:{item_id}")
    kb.button(text='Удалить', callback_data=f"delete:{item_id}")
    kb.adjust(3)
    return kb.as_markup()


def cart_confirm_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Заказать', callback_data=f"add_order")
    kb.button(text=f'Назад', callback_data=f"back_start:")
    kb.adjust(1)
    return kb.as_markup()


def cart_back_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Назад', callback_data=f"back_start:")
    kb.adjust(1)
    return kb.as_markup()