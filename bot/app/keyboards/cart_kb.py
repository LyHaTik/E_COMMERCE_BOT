from aiogram.utils.keyboard import InlineKeyboardBuilder


def item_ikb(cart_item):
    kb = InlineKeyboardBuilder()
    kb.button(text='-', callback_data=f"minus:{cart_item.id}")
    kb.button(text=f'{cart_item.quantity}', callback_data=f"заглушка")
    kb.button(text='+', callback_data=f"plus:{cart_item.id}")
    kb.button(text='Удалить', callback_data=f"delete:{cart_item.id}")
    kb.adjust(3)
    return kb.as_markup()


def cart_ikb():
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