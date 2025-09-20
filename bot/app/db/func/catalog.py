from sqlalchemy import select

from app.db.models import Category, Product
from app.db.connect import AsyncSessionLocal


async def get_categories():
    """Список категорий"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category))
        return result.scalars().all()


async def get_products_by_category(category_id: int):
    """Все товары выбранной категории"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.category_id == category_id)
        )
        return result.scalars().all()


async def get_product(product_id: int):
    """Детальная информация о товаре"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()