from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
def get_products():
    return {"message": "all products"}


@router.get("/{id}")
def get_product(id: int):
    return {"message": "product detail"}
