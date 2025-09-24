from shared.db.connect import engine, Base, AsyncSessionLocal
from shared.db.models import Category, Product


async def create_tables_if_not_exist() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT COUNT(*) FROM products;")
        count = result.scalar_one()

        if count == 0:
            category = Category(title="Спорт")
            session.add(category)
            await session.flush()

            products = [
                Product(
                    category_id=category.id,
                    title="Велосипед",
                    description="27 скоростей",
                    price=70000,
                    currency="RUB",
                    img_url="AgACAgUAAxkBAAIXs2jTwuQOTZIwAtusZdQraRLUdxXpAAI2yzEbRPehVhizsBl8BOLOAQADAgADeQADNgQ",
                    stock=10,
                ),
            ]
            session.add_all(products)

            await session.commit()