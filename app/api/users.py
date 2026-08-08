from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_users():
    return {"message": "all users"}


@router.get("/{id}")
def get_user(id: int):
    return {"message": "user detail"}
