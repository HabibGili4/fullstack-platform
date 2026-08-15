import pytest


class TestAdminProductFlow:
    def test_admin_crud_flow(self, client, admin_token):
        headers = {"Authorization": f"Bearer {admin_token}"}

        list_resp = client.get("/api/v1/products/", headers=headers)
        assert list_resp.status_code == 200

        create_resp = client.post(
            "/api/v1/products/",
            headers=headers,
            json={"name": "E2E Product", "description": "End to end test", "price": 250000.0},
        )
        assert create_resp.status_code == 201
        product_id = create_resp.json()["id"]

        get_resp = client.get(f"/api/v1/products/{product_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "E2E Product"

        update_resp = client.put(
            f"/api/v1/products/{product_id}",
            headers=headers,
            json={"name": "E2E Product Updated", "description": "Updated desc", "price": 300000.0},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "E2E Product Updated"

        delete_resp = client.delete(f"/api/v1/products/{product_id}", headers=headers)
        assert delete_resp.status_code == 200

        get_deleted = client.get(f"/api/v1/products/{product_id}", headers=headers)
        assert get_deleted.status_code == 404


class TestRbacDeniedFlow:
    def test_user_read_ok_create_denied(self, client, seeded_users):
        user_resp = client.post(
            "/api/v1/users/login",
            json={"email": "user@test.com", "password": "password123"},
        )
        user_headers = {"Authorization": f"Bearer {user_resp.json()['access_token']}"}

        get_resp = client.get("/api/v1/products/", headers=user_headers)
        assert get_resp.status_code == 200

        create_resp = client.post(
            "/api/v1/products/",
            headers=user_headers,
            json={"name": "Forbidden", "description": "Should fail", "price": 100.0},
        )
        assert create_resp.status_code == 403
