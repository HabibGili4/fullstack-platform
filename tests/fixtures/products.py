import pytest

from app.models.product_model import Product


@pytest.fixture()
def seeded_product(db, seeded_users):
    product = Product(
        name="Test Product",
        description="A test product",
        price=100000.00,
        owner_id=seeded_users["admin"].id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture()
def seeded_products(db, seeded_users):
    products = []
    items = [
        {"name": "Product A", "description": "First product", "price": 50000.00, "owner_id": seeded_users["admin"].id},
        {"name": "Product B", "description": "Second product", "price": 75000.00, "owner_id": seeded_users["editor"].id},
    ]
    for data in items:
        p = Product(**data)
        db.add(p)
        db.flush()
        products.append(p)
    db.commit()
    return products
