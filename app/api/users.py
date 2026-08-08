from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

users = [
    {"id": 1, "name": "Habib"},
    {"id": 2, "name": "Gillzz"},
]


@router.get("/")
def get_users(current_user: dict = Depends(get_current_user)):
    return {"users": users, "user": current_user}


@router.get("/{user_id}")
def get_user(user_id: int, current_user: dict = Depends(get_current_user)):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
    return {**user, "user": current_user}


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate):
    return body.model_dump()
