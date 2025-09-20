# catalog_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def categories_keyboard(categories):
    kb = InlineKeyboardMarkup(row_width=2)
    for cat in categories:
        kb.add(InlineKeyboardButton(text=cat.title, callback_data=f"cat:{cat.id}"))
    return kb

def product_keyboard(product_id):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("В корзину", callback_data=f"add:{product_id}"))
    kb.add(InlineKeyboardButton("Назад к категориям", callback_data="back:categories"))
    return kb
