import os

from sqlalchemy import select
from dotenv import load_dotenv

from db.connect import AsyncSessionLocal
from db.models import User


load_dotenv()
ADMINS = os.getenv("ADMINS")

async def get_or_create_user(user_id: int, name: str | None = None) -> User:
    """Проверяет, записывает и возвращает пользователя"""
    async with AsyncSessionLocal() as session:
        q = await session.execute(
            select(User)
            .where(User.id == user_id))
        user = q.scalar_one_or_none()
        if user:
            return user
        user = User(id=user_id, name=name, is_admin=False)
        if str(user_id) in ADMINS:
            user = User(id=user_id, name=name, is_admin=True)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    
async def put_user_contact(user_id: int, name: str, phone: str, address: str):
    """Записывает контакты и возвращает пользователя"""
    async with AsyncSessionLocal() as session:
        user = await session.get(User, user_id)
        if user:
            user.name = name
            user.phone = phone
            user.address = address
        else:
            user = User(
                id=user_id,
                name=name,
                phone=phone,
                address=address,
            )
            session.add(user)
        await session.commit()
        return user