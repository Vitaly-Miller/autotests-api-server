import uuid

from fastapi import HTTPException, status

from apps.users.schema.users import GetUserResponse, User, CreateUserRequest, UpdateUserRequest
from services.database.repositories.users import UsersRepository


async def get_user(user_id: uuid.UUID, users_repository: UsersRepository) -> GetUserResponse:
    user = await users_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return GetUserResponse(user=User.model_validate(user))


async def create_user(
        request: CreateUserRequest,
        users_repository: UsersRepository
) -> GetUserResponse:
    user = await users_repository.get_by_email(request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {request.email} already exists"
        )

    user = await users_repository.create(request.model_dump(mode='json'))

    return GetUserResponse(user=User.model_validate(user))


async def update_user(
        user_id: uuid.UUID,
        request: UpdateUserRequest,
        users_repository: UsersRepository
) -> GetUserResponse:
    user = await users_repository.get_by_email(request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {request.email} already exists"
        )

    user = await users_repository.update(
        user_id, request.model_dump(mode='json', exclude_unset=True)
    )

    return GetUserResponse(user=User.model_validate(user))


async def delete_user(user_id: uuid.UUID, users_repository: UsersRepository):
    await users_repository.delete(user_id)
