from aiogram.utils.keyboard import InlineKeyboardBuilder


def contact_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Подвердить', callback_data=f"confirm_contact:")
    kb.button(text=f'Изменить', callback_data=f"edit_contact:")
    kb.adjust(2)
    return kb.as_markup()


def delivery_method_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Почта', callback_data=f"Почта")
    kb.button(text=f'Курьер', callback_data=f"Курьер")
    kb.adjust(2)
    return kb.as_markup()