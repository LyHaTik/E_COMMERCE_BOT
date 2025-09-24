from aiogram.utils.keyboard import InlineKeyboardBuilder

from shared.db.models import Product, Category


def categories_ikb(categories: list[Category]):
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.button(
            text=c.title,
            callback_data=f"product_list:{c.id}"
        )
    kb.button(text=f'Назад', callback_data="back_start:")
    kb.adjust(1)
    return kb.as_markup()


def product_list_ikb(products: list[Product]):
    kb = InlineKeyboardBuilder()
    for p in products:
        kb.button(
                text=p.title,
                callback_data=f"product_details:{p.id}"
            )
    kb.button(text=f'Назад', callback_data="back_categories:")
    kb.adjust(1)
    return kb.as_markup()


def product_details_ikb(product_id: int, is_admin: bool):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'В корзину', callback_data=f"to_cart:{product_id}")
    if is_admin:
        kb.button(text=f'Изменить', callback_data=f"edit_product:{product_id}")
    kb.button(text=f'Назад', callback_data=f"back_product_list:{product_id}")
    kb.adjust(1)
    return kb.as_markup()
