from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_product_confirm_ikb():
    kb = InlineKeyboardBuilder()
    kb.button(text=f'Сохранить', callback_data=f"confirm_product:")
    kb.button(text=f'Отмена', callback_data=f"back_start:")
    kb.adjust(2)
    return kb.as_markup()


def add_product_category_kb(categories):
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.button(text=c.title, callback_data=c.title)
    kb.adjust(2)
    return kb.as_markup()