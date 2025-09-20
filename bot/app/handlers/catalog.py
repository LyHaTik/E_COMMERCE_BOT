"""
/start — приветствие + кнопка «Каталог товаров»

show_categories() — inline-кнопки категорий

show_products(category_id) — товары выбранной категории

show_product_detail(product_id) — фото, описание, цена, кнопка «В корзину»"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


router = Router()


# отображаем список категорий
@router.message(F.text == "Каталог товаров")
async def hand_categories(message: Message):
    pass

# отображаем товары
@router.callback_query(F.data.startswith("cat:"))
async def hand_products(callback: CallbackQuery):
    _, category_id = callback.data.split(":")

# детальня информация о товаре
@router.callback_query(F.data.startswith("prod:"))
async def hand_detail_product(callback: CallbackQuery):
    _, product_id = callback.data.split(":")
    # если админ допольнительно кнопку Изменить