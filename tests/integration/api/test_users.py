import pytest

from app.models.user_model import User
from tests.conftest import create_expired_token, create_invalid_signature_token


class TestGetMe:
    def test_me_valid_token(self, client, admin_token):
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@test.com"
        assert data["role"] == "admin"

    def test_me_no_token(self, client, seeded_users):
        resp = client.get("/api/v1/users/me")
        assert resp.status_code == 401

    def test_me_expired_token(self, client, seeded_users):
        expired_token = create_expired_token(user_id=1, role="admin")
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert resp.status_code == 401

    def test_me_invalid_signature(self, client, seeded_users):
        invalid_token = create_invalid_signature_token(user_id=1, role="admin")
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {invalid_token}"},
        )
        assert resp.status_code == 401


class TestRegister:
    def test_register_user(self, client, seeded_users):
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
        assert data["role"] == "user"


class TestGetUsers:
    def test_get_all_users(self, client, admin_token):
        resp = client.get(
            "/api/v1/users/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200

    def test_get_user_by_id(self, client, seeded_users, admin_token):
        user_id = seeded_users["admin"].id
        resp = client.get(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@test.com"


class TestUpdateUser:
    def test_update_user(self, client, seeded_users, admin_token):
        user_id = seeded_users["admin"].id
        resp = client.put(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"name": "Updated Admin", "email": "admin@test.com", "age": 30},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Updated Admin"


class TestDeleteUser:
    def test_delete_user(self, client, db, seeded_users, admin_token):
        client.post(
            "/api/v1/users/",
            json={"name": "To Delete", "email": "delete@test.com", "age": 25, "password": "password123"},
        )
        user = db.query(User).filter(User.email == "delete@test.com").first()
        user_id = user.id

        resp = client.delete(
            f"/api/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200
