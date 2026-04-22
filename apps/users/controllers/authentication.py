from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from apps.users.schema.authentication import TokenData, Token, LoginRequest, LoginResponse, RefreshRequest
from apps.users.schema.users import User
from config import settings
from services.database.repositories.users import UsersRepository, get_users_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/authentication/token")


def create_access_token(data: TokenData) -> str:
    data.expire = datetime.utcnow() + timedelta(seconds=settings.jwt_access_token_expire)
    return jwt.encode(
        data.model_dump(mode='json'), settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(data: TokenData) -> str:
    data.expire = datetime.utcnow() + timedelta(seconds=settings.jwt_refresh_token_expire)
    return jwt.encode(
        data.model_dump(mode='json'), settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def verify_token(token: str) -> TokenData | None:
    try:
        data = TokenData.model_validate(
            jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        )

        return data if data.expire >= datetime.utcnow() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None


async def login(request: LoginRequest, users_repository: UsersRepository) -> LoginResponse:
    user = await users_repository.verify_user(email=request.email, password=request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    data = TokenData(user_id=user.id)
    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)

    return LoginResponse(
        token=Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


async def refresh(request: RefreshRequest, users_repository: UsersRepository) -> LoginResponse:
    data = verify_token(request.refresh_token)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token"
        )

    user = await users_repository.get_by_id(data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token"
        )

    access_token = create_access_token(data=TokenData(user_id=user.id))

    return LoginResponse(
        token=Token(
            access_token=access_token,
            refresh_token=request.refresh_token
        )
    )


async def get_user_me(
        token: str = Depends(oauth2_scheme),
        users_repository: UsersRepository = Depends(get_users_repository),
) -> User:
    try:
        data = verify_token(token)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        user = await users_repository.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return User.model_validate(user)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
