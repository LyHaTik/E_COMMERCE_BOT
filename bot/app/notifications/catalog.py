from aiogram.types import CallbackQuery
from db.models import CartItem


async def notifity_to_cart(item: CartItem, callback: CallbackQuery):
    await callback.answer(
        f"Добавлено ✅\n\
        В Корзине {item.quantity}шт.", show_alert=True
        )
    

async def notifity_error(callback: CallbackQuery):
    await callback.answer("⚠️ Не добавлено. Повторите", show_alert=True)