from aiogram.types import CallbackQuery


async def notifity_error_count(stock: int, callback: CallbackQuery):
    await callback.answer(
        f"⚠️ Товара больше нет\n\
            Максимум: {stock}", show_alert=True
            )