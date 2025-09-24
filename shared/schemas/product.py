from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    category_title: str
    title: str
    description: Optional[str]
    price: int
    stock: int
    img_url: Optional[str] = None

class ProductEdit(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[int]
    stock: Optional[int]
    img_url: Optional[str] = None
    category_id: Optional[int] = None