import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.client import get_database_session
from services.database.models import FilesModel
from utils.clients.database.repository import BasePostgresRepository


class FilesRepository(BasePostgresRepository):
    model = FilesModel

    async def get_by_id(self, file_id: uuid.UUID) -> FilesModel | None:
        return await self.model.get(self.session, clause_filter=(self.model.id == file_id,))

    async def create(self, data: dict) -> FilesModel:
        return await self.model.create(self.session, **data)

    async def delete(self, file_id: uuid.UUID) -> None:
        return await self.model.delete(self.session, clause_filter=(self.model.id == file_id,))


async def get_files_repository(
        session: Annotated[AsyncSession, Depends(get_database_session)]
) -> FilesRepository:
    return FilesRepository(session=session)
