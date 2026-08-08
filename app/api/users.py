from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all()
    return {"users": users, "user": current_user}


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_by_id(user_id)
    return {"id": user.id, "name": user.name, "email": user.email, "age": user.age, "user": current_user}


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
