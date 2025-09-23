from aiogram.types import CallbackQuery


async def notifity_add_product(stock: int, callback: CallbackQuery):
    await callback.answer(
        f"Добавлено ✅\n\
        {stock}шт.", show_alert=True
        )


async def notifity_edit_product(stock: int, callback: CallbackQuery):
    await callback.answer(
        f"Изменен ✅\n\
        {stock}шт.", show_alert=True
        )


async def notifity_error(callback: CallbackQuery):
    await callback.answer("⚠️ Не добавлено. Повторите", show_alert=True)