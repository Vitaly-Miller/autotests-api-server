from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.users.controllers.authentication import login, refresh
from apps.users.schema.authentication import LoginRequest, LoginResponse, RefreshRequest
from services.database.repositories.users import UsersRepository, get_users_repository
from utils.routes import APIRoutes

authentication_router = APIRouter(
    prefix=APIRoutes.AUTHENTICATION,
    tags=[APIRoutes.AUTHENTICATION.as_tag()]
)


@authentication_router.post("/token", include_in_schema=False)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    request = LoginRequest(email=form_data.username, password=form_data.password)
    response = await login(request, users_repository)

    return {'access_token': response.token.access_token, 'token_type': 'bearer'}


@authentication_router.post('/login', response_model=LoginResponse)
async def login_view(
        request: LoginRequest,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await login(request, users_repository)


@authentication_router.post('/refresh', response_model=LoginResponse)
async def refresh_view(
        request: RefreshRequest,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository)],
):
    return await refresh(request, users_repository)
