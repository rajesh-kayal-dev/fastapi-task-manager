from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate, UserCreate
from pwdlib import PasswordHash

def create_task(db: Session, task_data: TaskCreate):
    task = Task(
        title=task_data.title,
        description=task_data.description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        return False

    db.delete(task)
    db.commit()
    return True

password_hash = PasswordHash.recommended()
def hash_password(password: str) -> str:
    return password_hash.hash(password)

def create_user(db: Session, user_data: UserCreate):
    existing_user = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email address already exists",
        )

    user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return user