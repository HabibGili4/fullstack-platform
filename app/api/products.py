from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_pagination, require_permission

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/", dependencies=[Depends(require_permission("product:read"))])
def get_products(
    pagination: dict = Depends(get_pagination),
    current_user: dict = Depends(get_current_user),
):
    return {**pagination, "user": current_user}


@router.get("/price/{price}", dependencies=[Depends(require_permission("product:read"))])
def get_product_by_price(price: float, current_user: dict = Depends(get_current_user)):
    return {"price": price, "user": current_user}


@router.get("/{product_id}", dependencies=[Depends(require_permission("product:read"))])
def get_product(product_id: int, current_user: dict = Depends(get_current_user)):
    return {"id": product_id, "user": current_user}


@router.post("/", dependencies=[Depends(require_permission("product:create"))])
def create_product(current_user: dict = Depends(get_current_user)):
    return {"message": "product created", "user": current_user}


@router.put("/{product_id}", dependencies=[Depends(require_permission("product:update"))])
def update_product(product_id: int, current_user: dict = Depends(get_current_user)):
    return {"message": "product updated", "id": product_id, "user": current_user}


@router.delete("/{product_id}", dependencies=[Depends(require_permission("product:delete"))])
def delete_product(product_id: int, current_user: dict = Depends(get_current_user)):
    return {"message": "product deleted", "id": product_id, "user": current_user}
