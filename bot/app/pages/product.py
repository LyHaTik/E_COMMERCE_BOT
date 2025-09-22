from aiogram.fsm.context import FSMContext

from auth import bot
from keyboards.product_kb import save_product_ikb, add_product_category_kb
from db.func.catalog import get_categories



async def edit_product_page(user_id: int, product_id: int, state: FSMContext):
    pass


async def add_product_category_page(user_id: int, state: FSMContext):
    categories = await get_categories()
    
    add_product_message = await bot.send_message(
        chat_id=user_id,
        text="Напишите или выберите название категории:",
        reply_markup=add_product_category_kb(categories)
        )

    await state.update_data(add_product_message_id=add_product_message.message_id)


async def add_product_title_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    add_product_message_id = data.get("add_product_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=add_product_message_id,
        text="Напишите название продукта:"
        )


async def add_product_description_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    add_product_message_id = data.get("add_product_message_id")
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=add_product_message_id,
        text="Напишите описание:"
        )
    
    
async def add_product_price_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    add_product_message_id = data.get("add_product_message_id")
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=add_product_message_id,
        text="Напишите цену:"
        )
    

async def add_product_stock_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    add_product_message_id = data.get("add_product_message_id")
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=add_product_message_id,
        text="Напишите кол-во:"
        )
  
    
async def add_product_img_page(user_id: int, state: FSMContext):
    data = await state.get_data()
    add_product_message_id = data.get("add_product_message_id")
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=add_product_message_id,
        text="Отправте фото:"
        )


async def add_product_page(
    user_id: int,
    category_title: str,
    product_title: str,
    product_description: str,
    product_price: int,
    product_stock: int,
    img_id: str,
    state: FSMContext
    ):
    message_product = await bot.send_photo(
        chat_id=user_id,
        photo=img_id,
        caption=f"Категория: {category_title}\n\
                Название: {product_title}\n\
                Описание: {product_description}\n\
                Цена: {product_price} RUB\n\
                Кол-во: {product_stock}",
        reply_markup=save_product_ikb()
        )
    
    await state.update_data(message_product_id=message_product.message_id)