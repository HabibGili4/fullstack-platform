import hashlib

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, name: str, email: str, age: int, password: str):
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
