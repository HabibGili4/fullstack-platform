import hashlib

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_all(self) -> list[User]:
        return self.repo.get_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
        return user

    def register(self, name: str, email: str, age: int, password: str) -> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = self.repo.create(
            name=name,
            email=email,
            age=age,
            password_hash=password_hash,
        )
        return user

    def update(self, user_id: int, data: dict) -> User:
        user = self.get_by_id(user_id)

        if "email" in data:
            existing = self.repo.get_by_email(data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Email sudah terdaftar")

        return self.repo.update(user, data)

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repo.delete(user)
