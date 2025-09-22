from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Category, Product
from db.connect import AsyncSessionLocal


async def get_categories():
    """Список категорий"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()


async def get_products_by_category(category_id: int):
    """Все товары выбранной категории"""
    print(category_id)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product)
            .where(Product.category_id == category_id)
        )
        return result.scalars().all()


async def get_product(product_id: int):
    """Детальная информация о товаре"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        return result.scalar_one_or_none()