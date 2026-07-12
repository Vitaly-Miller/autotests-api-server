from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from services.database.client import get_database_session
from services.database.models.courses import CoursesModel
from services.database.models.exercises import ExercisesModel
from services.database.models.files import FilesModel
from services.database.models.users import UsersModel
from services.database.repositories.users import UsersRepository
from utils.routes import APIRoutes

cleanup_router = APIRouter(
    prefix=APIRoutes.CLEANUP,
    tags=[APIRoutes.CLEANUP.as_tag()]
)


@cleanup_router.post("")
async def cleanup_view(session: Annotated[AsyncSession, Depends(get_database_session)]):
    await session.execute(delete(ExercisesModel))
    await session.execute(delete(CoursesModel))

    files = (await session.execute(select(FilesModel))).scalars().all()
    await session.execute(delete(FilesModel))

    await session.execute(delete(UsersModel))
    await session.commit()

    await UsersRepository(session=session).ensure_default_user()

    for file in files:
        file.system_file.unlink(missing_ok=True)
