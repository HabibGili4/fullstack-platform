from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users():
    return {"message": "all users"}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
