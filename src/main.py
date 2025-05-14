from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.products import router as products_router
from src.api.categories import router as categories_router
from src.api.purchases import router as purchases_router
from src.api.auth import router as auth_router
from src.api.manufacturers import router as manufacturers_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Babuin Enjoyer"}

app.include_router(products_router)
app.include_router(categories_router)
app.include_router(purchases_router)
app.include_router(auth_router)
app.include_router(manufacturers_router)