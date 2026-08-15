import pytest


class TestDatabaseConnection:
    def test_db_connection_via_me(self, client, admin_token):
        resp = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert resp.status_code == 200

    def test_db_session_cleanup(self, client, seeded_users, admin_token):
        for _ in range(3):
            resp = client.get(
                "/api/v1/users/me",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
            assert resp.status_code == 200
