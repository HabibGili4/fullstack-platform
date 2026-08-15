from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.services.user_service import UserService


@pytest.fixture
def mock_user_repo():
    return MagicMock()


@pytest.fixture
def mock_password_hasher():
    return MagicMock()


@pytest.fixture
def user_service(mock_user_repo, mock_password_hasher):
    svc = UserService.__new__(UserService)
    svc.db = MagicMock()
    svc.repo = mock_user_repo
    svc.pwd = mock_password_hasher
    return svc


class TestRegister:
    def test_register_success(self, user_service, mock_user_repo, mock_password_hasher):
        mock_user_repo.get_by_email.return_value = None
        fake_user = MagicMock()
        fake_user.email = "new@test.com"
        mock_user_repo.create.return_value = fake_user
        mock_password_hasher.hash.return_value = "hashed_pw"

        result = user_service.register("New User", "new@test.com", 22, "password123")

        assert result.email == "new@test.com"
        mock_password_hasher.hash.assert_called_once_with("password123")
        mock_user_repo.create.assert_called_once()

    def test_register_duplicate_email(self, user_service, mock_user_repo):
        existing_user = MagicMock()
        mock_user_repo.get_by_email.return_value = existing_user

        with pytest.raises(HTTPException) as exc_info:
            user_service.register("Dup User", "existing@test.com", 25, "password123")
        assert exc_info.value.status_code == 400


class TestGetById:
    def test_get_by_id_found(self, user_service, mock_user_repo):
        fake_user = MagicMock()
        fake_user.id = 1
        mock_user_repo.get_by_id.return_value = fake_user

        result = user_service.get_by_id(1)
        assert result.id == 1

    def test_get_by_id_not_found(self, user_service, mock_user_repo):
        mock_user_repo.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            user_service.get_by_id(999)
        assert exc_info.value.status_code == 404


class TestUpdate:
    def test_update_success(self, user_service, mock_user_repo):
        fake_user = MagicMock()
        fake_user.id = 1
        mock_user_repo.get_by_id.return_value = fake_user
        mock_user_repo.get_by_email.return_value = None
        updated_user = MagicMock()
        mock_user_repo.update.return_value = updated_user

        result = user_service.update(1, {"name": "Updated"})
        assert result == updated_user


class TestDelete:
    def test_delete_success(self, user_service, mock_user_repo):
        fake_user = MagicMock()
        fake_user.id = 1
        mock_user_repo.get_by_id.return_value = fake_user

        user_service.delete(1)
        mock_user_repo.delete.assert_called_once_with(fake_user)
