from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from apps.cleanup.api import cleanup_app_router
from apps.courses.api import courses_app_router
from apps.exercises.api import exercises_app_router
from apps.files.api import files_app_router
from apps.users.api import users_app_router
from services.database.repositories.users import UsersRepository
from utils.clients.database.engine import create_database, get_database_engine

app = FastAPI(title="QA Automation engineer course API")

app.mount("/static", StaticFiles(directory="storage"), name="static")

app.include_router(users_app_router, prefix="/api/v1")
app.include_router(files_app_router, prefix="/api/v1")
app.include_router(courses_app_router, prefix="/api/v1")
app.include_router(exercises_app_router, prefix="/api/v1")
app.include_router(cleanup_app_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    await create_database()

    async_session = await get_database_engine()
    async with async_session() as session:
        await UsersRepository(session=session).ensure_default_user()
