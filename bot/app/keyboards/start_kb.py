from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb(is_admin: bool):
    kb = [
        [KeyboardButton(text="Каталог товаров")],
        [KeyboardButton(text="Корзина")]
        ]
    if is_admin:
        kb.append([KeyboardButton(text="Добавить товар")])
        kb.append([KeyboardButton(text="Заказы")])

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def back_kb():
    kb = [[KeyboardButton(text="Назад")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)