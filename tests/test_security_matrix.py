import pytest

from tests.conftest import create_expired_token, create_invalid_signature_token


# ============================================================
# Scenario 1: Register
# ============================================================
class TestRegister:
    def test_register_201(self, client):
        resp = client.post(
            "/api/v1/users/",
            json={
                "name": "New User",
                "email": "new@test.com",
                "age": 22,
                "password": "password123",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "new@test.com"
        assert data["name"] == "New User"
        assert data["role"] == "user"
        assert "password" not in data
        assert "password_hash" not in data


# ============================================================
# Scenario 2: Login
# ============================================================
class TestLogin:
    def test_login_200(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password_401(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "wrongpassword"},
        )
        assert resp.status_code == 401

    def test_login_nonexistent_user_401(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "nobody@test.com", "password": "password123"},
        )
        assert resp.status_code == 401


# ============================================================
# Scenario 3: GET /me valid token
# ============================================================
class TestMeValidToken:
    def test_me_valid_token_200(self, client, admin_token):
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@test.com"
        assert data["role"] == "admin"


# ============================================================
# Scenario 4: GET /me no token
# ============================================================
class TestMeNoToken:
    def test_me_no_token_401(self, client, seeded_users):
        resp = client.get("/api/v1/users/me")
        assert resp.status_code == 401


# ============================================================
# Scenario 5: GET /me expired token
# ============================================================
class TestMeExpiredToken:
    def test_me_expired_token_401(self, client, seeded_users):
        expired_token = create_expired_token(user_id=1, role="admin")
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert resp.status_code == 401


# ============================================================
# Scenario 6: GET /me invalid signature
# ============================================================
class TestMeInvalidSignature:
    def test_me_invalid_signature_401(self, client, seeded_users):
        invalid_token = create_invalid_signature_token(user_id=1, role="admin")
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {invalid_token}"},
        )
        assert resp.status_code == 401


# ============================================================
# Scenario 7: DELETE product as Admin → 200
# ============================================================
class TestDeleteProductAdmin:
    def test_delete_product_admin_200(self, client, admin_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["message"] == "product deleted"
        assert data["id"] == seeded_product.id


# ============================================================
# Scenario 8: DELETE product as User → 403
# ============================================================
class TestDeleteProductUser:
    def test_delete_product_user_403(self, client, user_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert resp.status_code == 403


# ============================================================
# Scenario 9: DELETE product as Editor → 403
# ============================================================
class TestDeleteProductEditor:
    def test_delete_product_editor_403(self, client, editor_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {editor_token}"},
        )
        assert resp.status_code == 403


# ============================================================
# Scenario 10: DELETE product as Manager → 403
# ============================================================
class TestDeleteProductManager:
    def test_delete_product_manager_403(self, client, manager_token, seeded_product):
        resp = client.delete(
            f"/api/v1/products/{seeded_product.id}",
            headers={"Authorization": f"Bearer {manager_token}"},
        )
        assert resp.status_code == 403


# ============================================================
# Scenario 11: Refresh valid
# ============================================================
class TestRefreshValid:
    def test_refresh_valid_200(self, client, seeded_users):
        login_resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        refresh_token = login_resp.json()["refresh_token"]

        resp = client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": refresh_token},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"


# ============================================================
# Scenario 12: Refresh expired
# ============================================================
class TestRefreshExpired:
    def test_refresh_expired_401(self, client, seeded_users):
        expired_refresh = create_expired_token(user_id=1)
        resp = client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": expired_refresh},
        )
        assert resp.status_code == 401


# ============================================================
# Scenario 13: Refresh reused/old token
# ============================================================
class TestRefreshReused:
    def test_refresh_reused_401(self, client, seeded_users):
        login_resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        refresh_token = login_resp.json()["refresh_token"]

        client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": refresh_token},
        )

        resp = client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": refresh_token},
        )
        assert resp.status_code == 401
