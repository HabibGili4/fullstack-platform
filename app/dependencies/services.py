from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, get_token_service
from app.core.ports import IPasswordHasher, ITokenService
from app.models.user_model import User
from app.repositories.account_repository import AccountRepository
from app.repositories.post_repository import PostRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.password_hasher import PasswordHasher
from app.services.post_service import PostService
from app.services.product_service import ProductService
from app.services.task_service import TaskService
from app.services.account_service import AccountService
from app.services.user_service import UserService


def get_password_hasher() -> IPasswordHasher:
    return PasswordHasher()


def get_auth_service(
    db: Session = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(get_password_hasher),
    token_service: ITokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(db=db, password_hasher=password_hasher, token_service=token_service)


def get_user_service(
    db: Session = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(get_password_hasher),
) -> UserService:
    user_repo = UserRepository(db)
    return UserService(db=db, user_repo=user_repo, password_hasher=password_hasher)


def get_post_service(
    db: Session = Depends(get_db),
) -> PostService:
    post_repo = PostRepository(db)
    user_repo = UserRepository(db)
    return PostService(db=db, post_repo=post_repo, user_repo=user_repo)


def get_task_service(
    db: Session = Depends(get_db),
) -> TaskService:
    task_repo = TaskRepository(db)
    user_repo = UserRepository(db)
    return TaskService(db=db, task_repo=task_repo, user_repo=user_repo)


def get_account_service(
    db: Session = Depends(get_db),
) -> AccountService:
    account_repo = AccountRepository(db)
    return AccountService(db=db, account_repo=account_repo)


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    product_repo = ProductRepository(db)
    return ProductService(db=db, product_repo=product_repo)
