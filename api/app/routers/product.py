# api/routers/product.py
from fastapi import APIRouter, HTTPException

from shared.schemas.product import ProductCreate, ProductEdit
from shared.db.func.product import put_product, edit_product, delete_product, get_or_create_category


router = APIRouter(prefix="/admin/products", tags=["product_admin"])


@router.post("/", response_model=dict)
async def create_product(data: ProductCreate):
    category = await get_or_create_category(data.category_title)
    product = await put_product(
        category_id=category.id,
        title=data.title,
        description=data.description,
        price=data.price,
        stock=data.stock,
        img_url=data.img_url
    )
    return {"id": product.id, "title": product.title}

@router.patch("/{product_id}", response_model=dict)
async def update_product(product_id: int, data: ProductEdit):
    product = await edit_product(product_id, **data.dict(exclude_unset=True))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "title": product.title}

@router.delete("/{product_id}", response_model=dict)
async def remove_product(product_id: int):
    await delete_product(product_id)
    return {"status": "deleted"}
