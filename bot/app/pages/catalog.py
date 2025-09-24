from aiogram.fsm.context import FSMContext

from auth import bot
from keyboards.catalog_kb import categories_ikb, product_list_ikb, product_details_ikb
from shared.db.func.catalog import get_products_by_category, get_categories, get_product
from shared.db.func.user import get_or_create_user


async def categories_page(user_id: int, state: FSMContext):
    categories = await get_categories()
    
    message = await bot.send_message(
        chat_id=user_id,
        text="Выберите категорию:",
        reply_markup=categories_ikb(categories)
        )
    
    await state.update_data(catalog_message_id=message.message_id)


async def edit_categories_page(user_id: int, state: FSMContext):
    categories = await get_categories()
    
    data = await state.get_data()
    catalog_message_id = data.get("catalog_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=catalog_message_id,
        text="Выберите категорию:",
        reply_markup=categories_ikb(categories)
        )


async def product_list_page(user_id: int, category_id: int, state: FSMContext):
    products = await get_products_by_category(category_id)

    data = await state.get_data()
    catalog_message_id = data.get("catalog_message_id")
    
    await bot.edit_message_text(
        chat_id=user_id,
        message_id=catalog_message_id,
        text=f"Выберите товар",
        reply_markup=product_list_ikb(products)
        )


async def product_details_page(user_id: int, product_id: int, state: FSMContext):
    product = await get_product(product_id)
    user = await get_or_create_user(user_id)

    message = await bot.send_photo(
        chat_id=user_id,
        photo=product.img_url,
        caption=f"{product.title} - {product.price} {product.currency}\n\
            {product.description}",
        reply_markup=product_details_ikb(product.id, user.is_admin)
    )

    data = await state.get_data()
    product_messages = data.get("product_details_message_dict", {})
    product_messages[product.id] = message.message_id
    
    await state.update_data(product_details_message_dict=product_messages)
