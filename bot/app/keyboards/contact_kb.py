from aiogram.utils.keyboard import InlineKeyboardBuilder


def contact_confirm_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Подвердить', callback_data=f"confirm_contact:")
    kb.button(text=f'Изменить', callback_data=f"edit_contact:")
    kb.adjust(2)
    return kb.as_markup()
