from bot.app.handlers.product.add_product import router as admin_router
from app.handlers.cart import router as cart_router
from app.handlers.catalog import router as catalog_router
from bot.app.handlers.order.add_order import router as order_router


routers = [
    admin_router,
    cart_router,
    catalog_router,
    order_router
]
