from datetime import timedelta

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.auth_service import AuthService, create_access_token
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate(body.email, body.password)

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=UserListResponse)
def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all()
    return {"users": users, "user": {"id": current_user.id, "name": current_user.name}}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_by_id(user_id)
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.register(
        name=body.name,
        email=body.email,
        age=body.age,
        password=body.password,
    )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.update(
        user_id=user_id,
        data=body.model_dump(),
    )
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    service.delete(user_id)
    return {"message": "user berhasil dihapus"}
