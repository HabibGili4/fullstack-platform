from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.ports import IProductRepository


class ProductService:
    def __init__(self, db: Session, product_repo: IProductRepository):
        self.db = db
        self.repo = product_repo

    def get_all(self) -> list:
        return self.repo.get_all()

    def get_by_id(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="product tidak ditemukan")
        return product

    def get_by_owner_id(self, owner_id: int) -> list:
        return self.repo.get_by_owner_id(owner_id)

    def create(self, name: str, description: str, price: float, owner_id: int):
        return self.repo.create(name=name, description=description, price=price, owner_id=owner_id)

    def update(self, product_id: int, data: dict, current_user):
        product = self.get_by_id(product_id)
        if current_user.role != "admin" and product.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="tidak bisa update product orang lain")
        return self.repo.update(product, data)

    def delete(self, product_id: int, current_user) -> None:
        product = self.get_by_id(product_id)
        if current_user.role != "admin" and product.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="tidak bisa hapus product orang lain")
        self.repo.delete(product)
