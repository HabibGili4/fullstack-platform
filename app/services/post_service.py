from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.post_model import Post
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository


class PostService:
    def __init__(self, db: Session):
        self.repo = PostRepository(db)
        self.user_repo = UserRepository(db)

    def get_all(self) -> list[Post]:
        return self.repo.get_all()

    def get_by_id(self, post_id: int) -> Post:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="postingan tidak ditemukan")
        return post

    def get_by_user_id(self, user_id: int) -> list[Post]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
        return self.repo.get_by_user_id(user_id)

    def create(self, title: str, detail: str, user_id: int) -> Post:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
        return self.repo.create(title=title, detail=detail, user_id=user_id)

    def update(self, post_id: int, data: dict) -> Post:
        post = self.get_by_id(post_id)
        return self.repo.update(post, data)

    def delete(self, post_id: int) -> None:
        post = self.get_by_id(post_id)
        self.repo.delete(post)
