import uuid
from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.client import get_database_session
from services.database.models import ExercisesModel
from utils.clients.database.repository import BasePostgresRepository


class ExercisesRepository(BasePostgresRepository):
    model = ExercisesModel

    async def filter(self, course_id: uuid.UUID) -> Sequence[ExercisesModel]:
        return await self.model.filter(
            self.session, clause_filter=(self.model.course_id == course_id,)
        )

    async def get_by_id(self, exercise_id: uuid.UUID) -> ExercisesModel | None:
        return await self.model.get(self.session, clause_filter=(self.model.id == exercise_id,))

    async def create(self, data: dict) -> ExercisesModel:
        return await self.model.create(self.session, **data)

    async def update(self, exercise_id: uuid.UUID, data: dict) -> ExercisesModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.id == exercise_id,), **data
        )

    async def delete(self, exercise_id: uuid.UUID) -> None:
        return await self.model.delete(self.session, clause_filter=(self.model.id == exercise_id,))


async def get_exercises_repository(
        session: Annotated[AsyncSession, Depends(get_database_session)]
) -> ExercisesRepository:
    return ExercisesRepository(session=session)
