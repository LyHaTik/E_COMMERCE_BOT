# api/routers/user.py
from fastapi import APIRouter, HTTPException

from shared.schemas.user import UserOut, UserContact
from shared.db.func.user import put_user_contact, get_or_create_user
from shared.db.models import User


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    user: User = await get_or_create_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(
        id=user.id,
        name=user.name,
        phone=user.phone,
        address=user.address,
        is_admin=user.is_admin
    )


@router.post("/{user_id}/contact", response_model=UserOut)
async def set_user_contact(user_id: int, contact: UserContact):
    user: User = await put_user_contact(
        user_id=user_id,
        name=contact.name,
        phone=contact.phone,
        address=contact.address
    )
    return UserOut(
        id=user.id,
        name=user.name,
        phone=user.phone,
        address=user.address,
        is_admin=user.is_admin
    )
