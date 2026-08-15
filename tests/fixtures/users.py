import pytest
from jose import jwt

from app.core.config import settings
from app.models.user_model import User
from app.services.password_hasher import PasswordHasher

_pwd = PasswordHasher()

USERS_DATA = [
    {"name": "Admin User", "email": "admin@test.com", "age": 25, "password": "password123", "role": "admin"},
    {"name": "Manager User", "email": "manager@test.com", "age": 28, "password": "password123", "role": "manager"},
    {"name": "Editor User", "email": "editor@test.com", "age": 22, "password": "password123", "role": "editor"},
    {"name": "Regular User", "email": "user@test.com", "age": 20, "password": "password123", "role": "user"},
]


@pytest.fixture()
def seeded_users(db):
    users = {}
    for data in USERS_DATA:
        user = User(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            password_hash=_pwd.hash(data["password"]),
            role=data["role"],
        )
        db.add(user)
        db.flush()
        users[data["role"]] = user
    db.commit()
    return users


@pytest.fixture()
def admin_token(client, seeded_users):
    resp = client.post("/api/v1/users/login", json={"email": "admin@test.com", "password": "password123"})
    return resp.json()["access_token"]


@pytest.fixture()
def manager_token(client, seeded_users):
    resp = client.post("/api/v1/users/login", json={"email": "manager@test.com", "password": "password123"})
    return resp.json()["access_token"]


@pytest.fixture()
def editor_token(client, seeded_users):
    resp = client.post("/api/v1/users/login", json={"email": "editor@test.com", "password": "password123"})
    return resp.json()["access_token"]


@pytest.fixture()
def user_token(client, seeded_users):
    resp = client.post("/api/v1/users/login", json={"email": "user@test.com", "password": "password123"})
    return resp.json()["access_token"]


@pytest.fixture()
def admin_refresh_token(client, seeded_users):
    resp = client.post("/api/v1/users/login", json={"email": "admin@test.com", "password": "password123"})
    return resp.json()["refresh_token"]


def create_expired_token(user_id: int, role: str = "user") -> str:
    from datetime import datetime, timedelta, timezone
    to_encode = {"sub": str(user_id), "role": role}
    expire = datetime.now(timezone.utc) - timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_invalid_signature_token(user_id: int, role: str = "user") -> str:
    from datetime import datetime, timedelta, timezone
    to_encode = {"sub": str(user_id), "role": role}
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "wrong-secret-key", algorithm=settings.ALGORITHM)
