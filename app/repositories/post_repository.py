from sqlalchemy.orm import Session

from app.models.post_model import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Post]:
        return self.db.query(Post).all()

    def get_by_id(self, post_id: int) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_by_user_id(self, user_id: int) -> list[Post]:
        return self.db.query(Post).filter(Post.user_id == user_id).all()

    def create(self, title: str, detail: str, user_id: int) -> Post:
        post = Post(title=title, detail=detail, user_id=user_id)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post, data: dict) -> Post:
        for key, value in data.items():
            setattr(post, key, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()
