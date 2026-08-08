from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
def get_products():
    return {"message": "all products"}


@router.get("/price/{price}")
def get_product_by_price(price: float):
    return {"price": price}


@router.get("/{product_id}")
def get_product(product_id: int):
    return {"id": product_id}
