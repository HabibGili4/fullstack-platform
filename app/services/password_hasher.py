from passlib.context import CryptContext

from app.core.ports import IPasswordHasher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)
