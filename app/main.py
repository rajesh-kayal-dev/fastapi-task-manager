from fastapi import FastAPI
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router

app = FastAPI(title="Task Manager API")

app.include_router(tasks_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"message": "Task Manager API"}