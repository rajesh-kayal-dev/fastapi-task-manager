from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.models import User, Task
from app.database import SessionLocal
from app.crud import create_task, get_tasks, get_task_by_id, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=False,
        user_id=current_user.id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .all()
    )

@router.get("/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.put("/{task_id}")
def edit_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return update_task(db, task_id, data)


@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task(db, task_id)
    return {"message": "Task deleted successfully"}