import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from apps.users.controllers.authentication import get_user_me
from apps.users.controllers.users import get_user, create_user, update_user, delete_user
from apps.users.schema.users import GetUserResponse, CreateUserRequest, UpdateUserRequest, User
from services.database.repositories.users import UsersRepository, get_users_repository
from utils.routes import APIRoutes

users_router = APIRouter(
    prefix=APIRoutes.USERS,
    tags=[APIRoutes.USERS.as_tag()]
)


@users_router.get('/me', response_model=GetUserResponse)
async def get_user_me_view(me: Annotated[User, Depends(get_user_me)]):
    return GetUserResponse(user=me)


@users_router.get(
    '/{user_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetUserResponse,
)
async def get_user_view(
        user_id: uuid.UUID,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await get_user(user_id, users_repository)


@users_router.post('', response_model=GetUserResponse)
async def create_user_view(
        request: CreateUserRequest,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await create_user(request, users_repository)


@users_router.patch(
    '/{user_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetUserResponse
)
async def update_user_view(
        user_id: uuid.UUID,
        request: UpdateUserRequest,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await update_user(user_id, request, users_repository)


@users_router.delete('/{user_id}', dependencies=[Depends(get_user_me)])
async def delete_user_view(
        user_id: uuid.UUID,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await delete_user(user_id, users_repository)
