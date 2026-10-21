from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class UserCreate(BaseModel):
    name: str
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    username: str
    password: str