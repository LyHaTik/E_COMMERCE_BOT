from aiogram.types import CallbackQuery

from db.models import CartItem


async def notifity_error_count(cart_item: CartItem, callback: CallbackQuery):
    await callback.answer(
        f"⚠️ Товара больше нет\n\
            Максимум: {cart_item.product.stock}", show_alert=True
            )