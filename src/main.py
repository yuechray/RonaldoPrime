from fastapi import FastAPI
from src.api import auth
from src.api.categories import router as categories_router
from src.api.products   import router as products_router
from src.api.purchases  import router as purchases_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Babuin Enjoyer"}

app.include_router(auth.router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(purchases_router)