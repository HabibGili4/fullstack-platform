from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = UserRepository(db)
    users = repo.get_all()
    return {"users": users, "user": current_user}


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
    return {"id": user.id, "name": user.name, "user": current_user}


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
