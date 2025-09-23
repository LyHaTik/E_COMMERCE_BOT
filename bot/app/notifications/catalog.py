from aiogram.types import CallbackQuery


async def notifity_to_cart(quantity: int, callback: CallbackQuery):
    await callback.answer(
        f"Добавлено ✅\n\
        В Корзине {quantity}шт.", show_alert=True
        )
    

async def notifity_error(callback: CallbackQuery):
    await callback.answer("⚠️ Не добавлено. Повторите", show_alert=True)
    

async def notifity_tap(command: str, callback: CallbackQuery):
    await callback.answer(f"Выбрано: {command}")