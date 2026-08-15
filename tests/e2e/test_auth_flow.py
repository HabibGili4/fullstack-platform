import pytest


class TestFullAuthFlow:
    def test_register_login_me_refresh_me(self, client):
        register_resp = client.post(
            "/api/v1/users/",
            json={"name": "E2E User", "email": "e2e@test.com", "age": 25, "password": "password123"},
        )
        assert register_resp.status_code == 201

        login_resp = client.post(
            "/api/v1/users/login",
            json={"email": "e2e@test.com", "password": "password123"},
        )
        assert login_resp.status_code == 200
        tokens = login_resp.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        me_resp = client.get("/api/v1/users/me", headers=headers)
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "e2e@test.com"

        refresh_resp = client.post(
            "/api/v1/users/refresh",
            json={"refresh_token": tokens["refresh_token"]},
        )
        assert refresh_resp.status_code == 200
        new_tokens = refresh_resp.json()
        new_headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}

        me_resp2 = client.get("/api/v1/users/me", headers=new_headers)
        assert me_resp2.status_code == 200
        assert me_resp2.json()["email"] == "e2e@test.com"


class TestLoginRetryFlow:
    def test_login_wrong_then_correct(self, client, seeded_users):
        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "wrongpassword"},
        )
        assert resp.status_code == 401

        resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        assert resp.status_code == 200
        token = resp.json()["access_token"]

        me_resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "admin@test.com"


class TestMultiUserFlow:
    def test_two_users_independent_sessions(self, client, seeded_users):
        admin_resp = client.post(
            "/api/v1/users/login",
            json={"email": "admin@test.com", "password": "password123"},
        )
        user_resp = client.post(
            "/api/v1/users/login",
            json={"email": "user@test.com", "password": "password123"},
        )

        admin_headers = {"Authorization": f"Bearer {admin_resp.json()['access_token']}"}
        user_headers = {"Authorization": f"Bearer {user_resp.json()['access_token']}"}

        admin_me = client.get("/api/v1/users/me", headers=admin_headers)
        user_me = client.get("/api/v1/users/me", headers=user_headers)

        assert admin_me.status_code == 200
        assert admin_me.json()["role"] == "admin"
        assert user_me.status_code == 200
        assert user_me.json()["role"] == "user"
