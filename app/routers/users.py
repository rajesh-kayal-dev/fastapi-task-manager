from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta, timezone
from app.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from app.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.crud import create_user, authenticate_user
from app.schemas import UserCreate, UserResponse, LoginSchema
from app.routers.tasks import get_db
from app.utils.mail import send_email
from fastapi import BackgroundTasks

security = HTTPBearer()

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    new_user = create_user(db, user)

    background_tasks.add_task(
        send_email,
        to_email=new_user.email,
        subject="Welcome to Task Manager",
        body=(
            f"Hello {new_user.name},\n\n"
            "Your Task Manager account has been created successfully."
        ),
    )

    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    credentials: LoginSchema,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        credentials.username,
        credentials.password,
    )

    payload = {
        "id": user.id,
        "username": user.username,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return {"token": token}

@router.get("/is-auth", response_model=UserResponse)
def is_authenticated(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user_id = payload.get("id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user