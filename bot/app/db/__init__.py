from db.connect import engine, Base, AsyncSessionLocal
from db.models import Category, Product


async def create_tables_if_not_exist() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT COUNT(*) FROM products;")
        count = result.scalar_one()

        if count == 0:
            category = Category(title="Электроника")
            session.add(category)
            await session.flush()

            products = [
                Product(
                    category_id=category.id,
                    title="Смартфон",
                    description="Мощный смартфон с отличной камерой",
                    price=30000,
                    currency="RUB",
                    img_url="https://example.com/phone.jpg",
                    stock=10,
                ),
                Product(
                    category_id=category.id,
                    title="Ноутбук",
                    description="Легкий и быстрый ноутбук",
                    price=70000,
                    currency="RUB",
                    img_url="https://example.com/laptop.jpg",
                    stock=5,
                ),
            ]
            session.add_all(products)

            await session.commit()