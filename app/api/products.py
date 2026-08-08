from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_pagination

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
def get_products(
    pagination: dict = Depends(get_pagination),
    current_user: dict = Depends(get_current_user),
):
    return {**pagination, "user": current_user}


@router.get("/price/{price}")
def get_product_by_price(price: float, current_user: dict = Depends(get_current_user)):
    return {"price": price, "user": current_user}


@router.get("/{product_id}")
def get_product(product_id: int, current_user: dict = Depends(get_current_user)):
    return {"id": product_id, "user": current_user}
