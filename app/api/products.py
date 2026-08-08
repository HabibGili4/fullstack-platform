from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/")
def get_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    category: str = Query(default=None),
    search: str = Query(default=None),
):
    return {"page": page, "limit": limit, "category": category, "search": search}


@router.get("/price/{price}")
def get_product_by_price(price: float):
    return {"price": price}


@router.get("/{product_id}")
def get_product(product_id: int):
    return {"id": product_id}
