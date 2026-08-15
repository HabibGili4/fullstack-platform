from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import JWTError

from app.services.auth_service import AuthService


@pytest.fixture
def mock_user_repo():
    return MagicMock()


@pytest.fixture
def mock_refresh_token_repo():
    return MagicMock()


@pytest.fixture
def mock_password_hasher():
    return MagicMock()


@pytest.fixture
def mock_token_service():
    return MagicMock()


@pytest.fixture
def auth_service(mock_user_repo, mock_refresh_token_repo, mock_password_hasher, mock_token_service):
    svc = AuthService.__new__(AuthService)
    svc.user_repo = mock_user_repo
    svc.refresh_token_repo = mock_refresh_token_repo
    svc.pwd = mock_password_hasher
    svc.token = mock_token_service
    return svc


class TestAuthenticate:
    def test_authenticate_success(self, auth_service, mock_user_repo, mock_password_hasher, mock_token_service, mock_refresh_token_repo):
        fake_user = MagicMock()
        fake_user.id = 1
        fake_user.email = "test@test.com"
        fake_user.role = "user"

        mock_user_repo.get_by_email.return_value = fake_user
        mock_password_hasher.verify.return_value = True
        mock_token_service.create_access_token.return_value = "access_token_123"
        mock_token_service.create_refresh_token.return_value = "refresh_token_123"

        result = auth_service.authenticate("test@test.com", "password123")

        assert result["access_token"] == "access_token_123"
        assert result["refresh_token"] == "refresh_token_123"
        assert result["token_type"] == "bearer"
        mock_password_hasher.verify.assert_called_once_with("password123", fake_user.password_hash)

    def test_authenticate_wrong_email(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            auth_service.authenticate("nobody@test.com", "password123")
        assert exc_info.value.status_code == 401

    def test_authenticate_wrong_password(self, auth_service, mock_user_repo, mock_password_hasher):
        fake_user = MagicMock()
        fake_user.password_hash = "hashed_pw"
        mock_user_repo.get_by_email.return_value = fake_user
        mock_password_hasher.verify.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            auth_service.authenticate("test@test.com", "wrongpassword")
        assert exc_info.value.status_code == 401

    def test_authenticate_revokes_old_tokens(self, auth_service, mock_user_repo, mock_password_hasher, mock_token_service, mock_refresh_token_repo):
        fake_user = MagicMock()
        fake_user.id = 1
        fake_user.role = "user"
        mock_user_repo.get_by_email.return_value = fake_user
        mock_password_hasher.verify.return_value = True
        mock_token_service.create_access_token.return_value = "access"
        mock_token_service.create_refresh_token.return_value = "refresh"

        auth_service.authenticate("test@test.com", "password123")

        mock_refresh_token_repo.revoke_all_for_user.assert_called_once_with(1)


class TestRefresh:
    def test_refresh_success(self, auth_service, mock_token_service, mock_refresh_token_repo, mock_user_repo):
        mock_token_service.decode_token.return_value = {"sub": "1", "role": "user"}
        mock_refresh_token_repo.is_valid.return_value = True
        fake_user = MagicMock()
        fake_user.id = 1
        fake_user.role = "user"
        mock_user_repo.get_by_id.return_value = fake_user
        mock_token_service.create_access_token.return_value = "new_access"
        mock_token_service.create_refresh_token.return_value = "new_refresh"

        result = auth_service.refresh("old_refresh_token")

        assert result["access_token"] == "new_access"
        assert result["refresh_token"] == "new_refresh"
        mock_refresh_token_repo.revoke.assert_called_once_with("old_refresh_token")

    def test_refresh_expired_token(self, auth_service, mock_token_service):
        mock_token_service.decode_token.side_effect = JWTError("Token expired")

        with pytest.raises(HTTPException) as exc_info:
            auth_service.refresh("expired_token")
        assert exc_info.value.status_code == 401

    def test_refresh_reused_token(self, auth_service, mock_token_service, mock_refresh_token_repo):
        mock_token_service.decode_token.return_value = {"sub": "1", "role": "user"}
        mock_refresh_token_repo.is_valid.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            auth_service.refresh("reused_token")
        assert exc_info.value.status_code == 401
