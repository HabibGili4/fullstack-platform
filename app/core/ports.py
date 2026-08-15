from abc import ABC, abstractmethod
from datetime import timedelta

from sqlalchemy.orm import Session


# ──────────────────────────────────────────────
# Password Hasher Port
# ──────────────────────────────────────────────


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, plain: str, hashed: str) -> bool: ...


# ──────────────────────────────────────────────
# Token Service Port
# ──────────────────────────────────────────────


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...


# ──────────────────────────────────────────────
# Base Repository (default CRUD)
# ──────────────────────────────────────────────


class BaseRepository:
    """Base class dengan default CRUD implementation.
    Concrete repos inherit ini + interface untuk satisfy contract.
    """

    def __init__(self, db: Session, model: type):
        self.db = db
        self.model = model

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self):
        return self.db.query(self.model).all()

    def create(self, **kwargs):
        entity = self.model(**kwargs)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity, data: dict):
        for key, value in data.items():
            setattr(entity, key, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity):
        self.db.delete(entity)
        self.db.commit()


# ──────────────────────────────────────────────
# Repository Ports (Interfaces)
# ──────────────────────────────────────────────


class IUserRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def get_all(self) -> list: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> object | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> object | None: ...

    @abstractmethod
    def create(
        self, name: str, email: str, age: int, password_hash: str, role: str = "user"
    ) -> object: ...

    @abstractmethod
    def update(self, user: object, data: dict) -> object: ...

    @abstractmethod
    def delete(self, user: object) -> None: ...


class IPostRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def get_all(self) -> list: ...

    @abstractmethod
    def get_by_id(self, post_id: int) -> object | None: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list: ...

    @abstractmethod
    def create(self, title: str, detail: str, user_id: int) -> object: ...

    @abstractmethod
    def update(self, post: object, data: dict) -> object: ...

    @abstractmethod
    def delete(self, post: object) -> None: ...


class ITaskRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def get_all(self) -> list: ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> object | None: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> list: ...

    @abstractmethod
    def create(
        self, title: str, detail: str, status: str, user_id: int
    ) -> object: ...

    @abstractmethod
    def update(self, task: object, data: dict) -> object: ...

    @abstractmethod
    def delete(self, task: object) -> None: ...


class IProductRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def get_all(self) -> list: ...

    @abstractmethod
    def get_by_id(self, product_id: int) -> object | None: ...

    @abstractmethod
    def get_by_owner_id(self, owner_id: int) -> list: ...

    @abstractmethod
    def create(self, name: str, description: str, price: float, owner_id: int) -> object: ...

    @abstractmethod
    def update(self, product: object, data: dict) -> object: ...

    @abstractmethod
    def delete(self, product: object) -> None: ...


class IAccountRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def get_by_id(self, account_id: int) -> object | None: ...

    @abstractmethod
    def get_by_id_for_update(self, account_id: int) -> object | None: ...

    @abstractmethod
    def update_balance(self, account: object, new_balance: float) -> object: ...


class IRefreshTokenRepository(ABC):
    @abstractmethod
    def __init__(self, db: Session): ...

    @abstractmethod
    def create(
        self, user_id: int, token: str, expires_at: object
    ) -> object: ...

    @abstractmethod
    def get_by_token(self, token: str) -> object | None: ...

    @abstractmethod
    def revoke_all_for_user(self, user_id: int) -> None: ...

    @abstractmethod
    def revoke(self, token: str) -> None: ...

    @abstractmethod
    def is_valid(self, token: str) -> bool: ...
