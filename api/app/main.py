from fastapi import FastAPI
from routers import cart, catalog, order, product, user
import uvicorn


app = FastAPI(
    title="E-Commerce API",
    description="API для взаимодействия с ботом и внешними сервисами",
    version="1.0.0",
)


app.include_router(cart.router)
app.include_router(catalog.router)
app.include_router(order.router)
app.include_router(product.router)
app.include_router(user.router)


#if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)