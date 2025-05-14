from fastapi import FastAPI
from src.api import auth
from src.api.categories import router as categories_router
from src.api.products   import router as products_router

app = FastAPI()

app.include_router(auth.router)
app.include_router(categories_router)
app.include_router(products_router)