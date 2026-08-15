import pytest

from tests.conftest import create_expired_token


class TestLogin:
    def test_login_success(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "wrongpassword"},
        )
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "nobody@test.com", "password": "password123"},
        )
        assert resp.status_code == 401


class TestRefresh:
    def test_refresh_success(self, client, seeded_users):
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

    def test_refresh_expired_token(self, client, seeded_users):
        expired_refresh = create_expired_token(user_id=1)
        resp = client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": expired_refresh},
        )
        assert resp.status_code == 401

    def test_refresh_reused_token(self, client, seeded_users):
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
