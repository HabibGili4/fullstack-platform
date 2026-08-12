from sqlalchemy.orm import Session

from app.models.task_model import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Task]:
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_user_id(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def create(self, title: str, detail: str, status: str, user_id: int) -> Task:
        task = Task(title=title, detail=detail, status=status, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task, data: dict) -> Task:
        for key, value in data.items():
            setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
