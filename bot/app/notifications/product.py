from aiogram.types import CallbackQuery

from db.models import Product


async def notifity_add_product(product: Product, callback: CallbackQuery):
    await callback.answer(
        f"Добавлено ✅\n\
        {product.title} - {product.stock}шт.", show_alert=True
        )

async def notifity_edit_product(product: Product, callback: CallbackQuery):
    await callback.answer(
        f"Изменен ✅\n\
        {product.title} - {product.stock}шт.", show_alert=True
        )

async def notifity_error(callback: CallbackQuery):
    await callback.answer("⚠️ Не добавлено. Повторите", show_alert=True)