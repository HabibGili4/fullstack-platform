from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
def get_posts(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_all()


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_by_id(post_id)


@router.get("/user/{user_id}", response_model=list[PostResponse])
def get_posts_by_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = PostService(db)
    return service.get_by_user_id(user_id)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(body: PostCreate, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.create(
        title=body.title,
        detail=body.detail,
        user_id=body.user_id,
    )


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, body: PostUpdate, db: Session = Depends(get_db)):
    service = PostService(db)
    return service.update(
        post_id=post_id,
        data=body.model_dump(),
    )


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    service = PostService(db)
    service.delete(post_id)
    return {"message": "postingan berhasil dihapus"}
