from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.user_model import User
from app.models.post_model import Post  # noqa: F401 — pastikan relasi terdeteksi
from app.models.task_model import Task  # noqa: F401 — pastikan relasi terdeteksi
from app.services.auth_service import pwd_context

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

users = [
    {"name": "Admin User", "email": "admin@test.com", "age": 25, "password": "password123", "role": "admin"},
    {"name": "Manager User", "email": "manager@test.com", "age": 28, "password": "password123", "role": "manager"},
    {"name": "Editor User", "email": "editor@test.com", "age": 22, "password": "password123", "role": "editor"},
    {"name": "Regular User", "email": "user@test.com", "age": 20, "password": "password123", "role": "user"},
]

db = SessionLocal()
try:
    for user_data in users:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"User {user_data['email']} sudah ada. Skip.")
        else:
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                age=user_data["age"],
                password_hash=pwd_context.hash(user_data["password"]),
                role=user_data["role"],
            )
            db.add(user)
            print(f"User {user_data['email']} ({user_data['role']}) berhasil ditambahkan.")
    db.commit()
    print("\nSeed data selesai!")
finally:
    db.close()
