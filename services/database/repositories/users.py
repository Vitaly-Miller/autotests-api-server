import uuid
from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.client import get_database_session
from services.database.models import UsersModel
from utils.clients.database.repository import BasePostgresRepository

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_USER_EMAIL = "user@example.com"
DEFAULT_USER_PASSWORD = "string"


class UsersRepository(BasePostgresRepository):
    model = UsersModel

    async def get_by_id(self, user_id: uuid.UUID) -> UsersModel | None:
        return await self.model.get(self.session, clause_filter=(self.model.id == user_id,))

    async def get_by_email(self, email: str) -> UsersModel | None:
        return await self.model.get(self.session, clause_filter=(self.model.email == email,))

    async def create(self, data: dict) -> UsersModel:
        data['password'] = password_context.hash(data['password'])

        return await self.model.create(self.session, **data)

    async def update(self, user_id: uuid.UUID, data: dict) -> UsersModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.id == user_id,), **data
        )

    async def delete(self, user_id: uuid.UUID) -> None:
        return await self.model.delete(self.session, clause_filter=(self.model.id == user_id,))

    async def verify_user(self, email: str, password: str) -> UsersModel | None:
        user = await self.get_by_email(email)
        if not user:
            return None

        if not password_context.verify(password, user.password):
            return None

        return user

    async def ensure_default_user(self) -> UsersModel:
        user = await self.get_by_email(DEFAULT_USER_EMAIL)
        if user:
            return user

        return await self.create({
            "email": DEFAULT_USER_EMAIL,
            "password": DEFAULT_USER_PASSWORD,
            "last_name": "Default",
            "first_name": "Default",
            "middle_name": "Default",
        })


async def get_users_repository(
        session: Annotated[AsyncSession, Depends(get_database_session)]
) -> UsersRepository:
    return UsersRepository(session=session)
