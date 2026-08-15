from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.services.product_service import ProductService


@pytest.fixture
def mock_product_repo():
    return MagicMock()


@pytest.fixture
def product_service(mock_product_repo):
    svc = ProductService.__new__(ProductService)
    svc.db = MagicMock()
    svc.repo = mock_product_repo
    return svc


class TestGetAll:
    def test_get_all(self, product_service, mock_product_repo):
        mock_product_repo.get_all.return_value = [{"id": 1}, {"id": 2}]
        result = product_service.get_all()
        assert len(result) == 2


class TestGetById:
    def test_get_by_id_found(self, product_service, mock_product_repo):
        fake_product = MagicMock()
        fake_product.id = 1
        mock_product_repo.get_by_id.return_value = fake_product

        result = product_service.get_by_id(1)
        assert result.id == 1

    def test_get_by_id_not_found(self, product_service, mock_product_repo):
        mock_product_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            product_service.get_by_id(999)
        assert exc_info.value.status_code == 404


class TestCreate:
    def test_create_product(self, product_service, mock_product_repo):
        fake_product = MagicMock()
        fake_product.name = "New Product"
        mock_product_repo.create.return_value = fake_product

        result = product_service.create("New Product", "Description", 50000.0, 1)
        assert result.name == "New Product"
        mock_product_repo.create.assert_called_once_with(
            name="New Product", description="Description", price=50000.0, owner_id=1
        )


class TestDelete:
    def test_delete_product(self, product_service, mock_product_repo):
        fake_product = MagicMock()
        fake_product.id = 1
        fake_product.owner_id = 1
        mock_product_repo.get_by_id.return_value = fake_product

        current_user = MagicMock()
        current_user.id = 1
        current_user.role = "admin"

        product_service.delete(1, current_user)
        mock_product_repo.delete.assert_called_once_with(fake_product)

    def test_delete_not_owner(self, product_service, mock_product_repo):
        fake_product = MagicMock()
        fake_product.owner_id = 1
        mock_product_repo.get_by_id.return_value = fake_product

        current_user = MagicMock()
        current_user.id = 2
        current_user.role = "editor"

        with pytest.raises(HTTPException) as exc_info:
            product_service.delete(1, current_user)
        assert exc_info.value.status_code == 403
