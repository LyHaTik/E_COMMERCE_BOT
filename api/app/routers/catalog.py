# api/routers/catalog.py
from fastapi import APIRouter, HTTPException
from typing import List

from shared.schemas.catalog import serialize_category, serialize_product
from shared.db.func.catalog import get_categories, get_products_by_category, get_product


router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("/categories", response_model=List[dict])
async def list_categories():
    categories = await get_categories()
    return [serialize_category(c) for c in categories]


@router.get("/categories/{category_id}/products", response_model=List[dict])
async def list_products(category_id: int):
    products = await get_products_by_category(category_id)
    return [serialize_product(p) for p in products]


@router.get("/products/{product_id}", response_model=dict)
async def product_detail(product_id: int):
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)
