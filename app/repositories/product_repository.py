from sqlalchemy.orm import Session

from app.core.ports import BaseRepository, IProductRepository
from app.models.product_model import Product


class ProductRepository(BaseRepository, IProductRepository):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_by_owner_id(self, owner_id: int) -> list[Product]:
        return self.db.query(Product).filter(Product.owner_id == owner_id).all()

    def create(self, name: str, description: str, price: float, owner_id: int) -> Product:
        return super().create(name=name, description=description, price=price, owner_id=owner_id)
