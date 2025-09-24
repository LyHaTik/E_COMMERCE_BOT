from pydantic import BaseModel


class UserContact(BaseModel):
    name: str
    phone: str
    address: str


class UserOut(BaseModel):
    id: int
    name: str | None
    phone: str | None
    address: str | None
    is_admin: bool