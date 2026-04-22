from fastapi import APIRouter

from apps.users.api.authentication import authentication_router
from apps.users.api.users import users_router

users_app_router = APIRouter()
users_app_router.include_router(users_router)
users_app_router.include_router(authentication_router)
