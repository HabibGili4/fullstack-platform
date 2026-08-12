from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.task_model import Task
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository


class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)
        self.user_repo = UserRepository(db)

    def get_all(self) -> list[Task]:
        return self.repo.get_all()

    def get_by_id(self, task_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="task tidak ditemukan")
        return task

    def get_by_user_id(self, user_id: int) -> list[Task]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
        return self.repo.get_by_user_id(user_id)

    def create(self, title: str, detail: str, status: str, user_id: int) -> Task:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="pengguna tidak ditemukan")
        return self.repo.create(title=title, detail=detail, status=status, user_id=user_id)

    def update(self, task_id: int, data: dict) -> Task:
        task = self.get_by_id(task_id)
        return self.repo.update(task, data)

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        self.repo.delete(task)
