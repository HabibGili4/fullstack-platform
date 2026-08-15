import pytest


class TestGetProducts:
    def test_get_products_admin(self, client, admin_token):
        resp = client.get(
            "/api/v1/products/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestCreateProduct:
    def test_create_product_admin(self, client, admin_token):
        resp = client.post(
            "/api/v1/products/",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"name": "Admin Product", "description": "Created by admin", "price": 100000.0},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Admin Product"
        assert data["owner_id"] is not None

    def test_create_product_user(self, client, user_token):
        resp = client.post(
            "/api/v1/products/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"name": "User Product", "description": "Should fail", "price": 50000.0},
        )
        assert resp.status_code == 403


class TestDeleteProduct:
    def test_delete_product_admin(self, client, admin_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["message"] == "product deleted"

    def test_delete_product_editor_not_owner(self, client, editor_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {editor_token}"},
        )
        assert resp.status_code == 403
