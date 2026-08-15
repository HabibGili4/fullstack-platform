from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models import Base
from app.models.user_model import User
from app.models.product_model import Product
from app.services.password_hasher import PasswordHasher
from app.services.token_service import TokenService

_pwd = PasswordHasher()
_token_svc = TokenService()

TEST_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded_users(db):
    users_data = [
        {"name": "Admin User", "email": "admin@test.com", "age": 25, "password": "password123", "role": "admin"},
        {"name": "Manager User", "email": "manager@test.com", "age": 28, "password": "password123", "role": "manager"},
        {"name": "Editor User", "email": "editor@test.com", "age": 22, "password": "password123", "role": "editor"},
        {"name": "Regular User", "email": "user@test.com", "age": 20, "password": "password123", "role": "user"},
    ]
    users = {}
    for data in users_data:
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
def seeded_product(db, seeded_users):
    product = Product(
        name="Test Product",
        description="A test product",
        price=100000.00,
        owner_id=seeded_users["admin"].id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


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
    to_encode = {"sub": str(user_id), "role": role}
    expire = datetime.now(timezone.utc) - timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_invalid_signature_token(user_id: int, role: str = "user") -> str:
    to_encode = {"sub": str(user_id), "role": role}
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "wrong-secret-key", algorithm=settings.ALGORITHM)
