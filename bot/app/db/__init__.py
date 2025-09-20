from app.db.connect import engine, Base


async def create_tables_if_not_exist() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)