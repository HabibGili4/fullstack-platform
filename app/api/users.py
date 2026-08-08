from fastapi import APIRouter, status

from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users():
    return {"message": "all users"}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate):
    return body.model_dump()
