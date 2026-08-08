from fastapi import FastAPI

from app.api.users import router as users_router
from app.api.products import router as products_router
from app.api.health import router as health_router

app = FastAPI()

app.include_router(users_router)
app.include_router(products_router)
app.include_router(health_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
