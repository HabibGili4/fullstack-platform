import pytest

from app.models.product_model import Product
from app.repositories.product_repository import ProductRepository


class TestProductRepository:
    def test_create_product(self, db, seeded_users):
        repo = ProductRepository(db)
        product = repo.create(
            name="Test Product",
            description="A test product",
            price=99000.00,
            owner_id=seeded_users["admin"].id,
        )
        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 99000.00
        assert product.owner_id == seeded_users["admin"].id

    def test_get_by_owner_id(self, db, seeded_users):
        repo = ProductRepository(db)
        repo.create(name="Product 1", description="Desc 1", price=10000.0, owner_id=seeded_users["admin"].id)
        repo.create(name="Product 2", description="Desc 2", price=20000.0, owner_id=seeded_users["admin"].id)
        repo.create(name="Product 3", description="Desc 3", price=30000.0, owner_id=seeded_users["editor"].id)

        products = repo.get_by_owner_id(seeded_users["admin"].id)
        assert len(products) == 2

    def test_get_by_id(self, db, seeded_users):
        repo = ProductRepository(db)
        product = repo.create(name="Find Me", description="Find", price=5000.0, owner_id=seeded_users["admin"].id)

        found = repo.get_by_id(product.id)
        assert found is not None
        assert found.name == "Find Me"
