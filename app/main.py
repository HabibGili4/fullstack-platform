from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.posts import router as posts_router
from app.api.products import router as products_router
from app.api.users import router as users_router
from app.core.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(posts_router)
app.include_router(products_router)
app.include_router(users_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
