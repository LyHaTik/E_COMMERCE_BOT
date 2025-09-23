from handlers.product import router as product_router
from handlers.cart import router as cart_router
from handlers.catalog import router as catalog_router
from handlers.order import router as order_router
from handlers.start import router as start_router


routers = [
    start_router,
    product_router,
    cart_router,
    catalog_router,
    order_router
]
