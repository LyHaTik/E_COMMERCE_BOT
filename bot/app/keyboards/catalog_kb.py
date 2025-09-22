from aiogram.utils.keyboard import InlineKeyboardBuilder


def categories_ikb(categories):
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.button(
            text=c.title,
            callback_data=f"product_list:{c.id}"
        )
    kb.button(text=f'Назад', callback_data=f"back_start:")
    kb.adjust(1)
    return kb.as_markup()


def product_list_ikb(products):
    kb = InlineKeyboardBuilder()
    for p in products:
        kb.button(
                text=f"{p.title}",
                callback_data=f"product_details:{p.id}"
            )
    kb.button(text=f'Назад', callback_data=f"back_categories:")
    kb.adjust(1)
    return kb.as_markup()


def product_ikb(product):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'В корзину', callback_data=f"to_cart:{product.id}")
    kb.button(text=f'Назад', callback_data=f"back_product_list:{product.id}")
    kb.adjust(1)
    return kb.as_markup()


def admin_product_ikb(product):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'В корзину', callback_data=f"to_cart:{product.id}")
    kb.button(text=f'Изменить', callback_data=f"edit_product:{product.id}")
    kb.button(text=f'Назад', callback_data=f"back_product_list:{product.id}")
    kb.adjust(2)
    return kb.as_markup()