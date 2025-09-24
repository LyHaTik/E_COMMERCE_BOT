from shared.db.models import Category, Product


def serialize_category(cat: Category):
    return {
        "id": cat.id,
        "title": cat.title
    }

def serialize_product(prod: Product):
    return {
        "id": prod.id,
        "title": prod.title,
        "description": prod.description,
        "price": prod.price,
        "currency": prod.currency,
        "img_url": prod.img_url,
        "stock": prod.stock,
        "category": prod.category_id
    }