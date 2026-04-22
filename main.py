from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from apps.courses.api import courses_app_router
from apps.exercises.api import exercises_app_router
from apps.files.api import files_app_router
from apps.users.api import users_app_router
from utils.clients.database.engine import create_database

app = FastAPI(title="QA Automation engineer course API")

app.mount("/static", StaticFiles(directory="storage"), name="static")

app.include_router(users_app_router, prefix="/api/v1")
app.include_router(files_app_router, prefix="/api/v1")
app.include_router(courses_app_router, prefix="/api/v1")
app.include_router(exercises_app_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    await create_database()
