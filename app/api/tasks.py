from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user, require_permission
from app.models.user_model import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse], dependencies=[Depends(require_permission("task:view"))])
def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_all()


@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(require_permission("task:view"))])
def get_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_by_id(task_id)


@router.get("/user/{user_id}", response_model=list[TaskResponse], dependencies=[Depends(require_permission("task:view"))])
def get_tasks_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.get_by_user_id(user_id)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("task:create"))])
def create_task(body: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.create(
        title=body.title,
        detail=body.detail,
        status=body.status,
        user_id=current_user.id,
    )


@router.put("/{task_id}", response_model=TaskResponse, dependencies=[Depends(require_permission("task:update"))])
def update_task(task_id: int, body: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    return service.update(
        task_id=task_id,
        data=body.model_dump(),
    )


@router.delete("/{task_id}", dependencies=[Depends(require_permission("task:delete"))])
def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = TaskService(db)
    service.delete(task_id)
    return {"message": "task berhasil dihapus"}
