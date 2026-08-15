from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_permission
from app.dependencies.services import get_product_service
from app.models.user_model import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse], dependencies=[Depends(require_permission("product:read"))])
def get_products(
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.get_all()


@router.get("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_permission("product:read"))])
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.get_by_id(product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("product:create"))])
def create_product(
    body: ProductCreate,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.create(
        name=body.name,
        description=body.description,
        price=body.price,
        owner_id=current_user.id,
    )


@router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_permission("product:update"))])
def update_product(
    product_id: int,
    body: ProductUpdate,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.update(
        product_id=product_id,
        data=body.model_dump(),
        current_user=current_user,
    )


@router.delete("/{product_id}", dependencies=[Depends(require_permission("product:delete"))])
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    service.delete(product_id=product_id, current_user=current_user)
    return {"message": "product deleted", "id": product_id}
