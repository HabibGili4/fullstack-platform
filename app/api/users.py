from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users(current_user: dict = Depends(get_current_user)):
    return {"message": "all users", "user": current_user}


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    return {"id": user_id, "user": current_user}


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate):
    return body.model_dump()
