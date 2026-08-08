from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
def get_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    category: str = Query(default=None),
    search: str = Query(default=None),
    current_user: dict = Depends(get_current_user),
):
    return {"page": page, "limit": limit, "category": category, "search": search, "user": current_user}


@router.get("/price/{price}")
def get_product_by_price(price: float, current_user: dict = Depends(get_current_user)):
    return {"price": price, "user": current_user}


@router.get("/{product_id}")
def get_product(product_id: int, current_user: dict = Depends(get_current_user)):
    return {"id": product_id, "user": current_user}
