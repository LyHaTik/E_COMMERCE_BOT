from sqlalchemy import select

from shared.db.models import Product, Category
from shared.db.connect import AsyncSessionLocal


async def get_or_create_category(title: str) -> Category:
    async with AsyncSessionLocal() as session:  
        result = await session.execute(
            select(Category).where(Category.title == title)
        )
        category = result.scalar_one_or_none()

        if category:
            return category

        category = Category(title=title)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category


async def put_product(category_id: int, title: str, description: str, price: int, stock: int, img_url: str = None):
    """Добавление товара"""
    async with AsyncSessionLocal() as session:
        product = Product(
            category_id=category_id,
            title=title,
            description=description,
            price=price,
            stock=stock,
            img_url=img_url,
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product


async def edit_product(product_id: int, **kwargs):
    """Редактирование товара"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return None
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        await session.commit()
        return product


async def delete_product(product_id: int):
    """Удаление товара"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if product:
            await session.delete(product)
            await session.commit()
