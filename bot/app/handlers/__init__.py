from handlers.product.add_product import router as add_product_router
from handlers.product.edit_product import router as edit_product_router
from handlers.cart import router as cart_router
from handlers.catalog import router as catalog_router
from handlers.order.add_order import router as add_order_router
from handlers.start import router as start_router
from handlers.test import router as test_router
from handlers.order.orders import router as orders_router


routers = [
    start_router,
    add_product_router,
    edit_product_router,
    cart_router,
    catalog_router,
    add_order_router,
    test_router,
    orders_router
]
