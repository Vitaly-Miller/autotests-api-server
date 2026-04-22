from fastapi import APIRouter

from apps.files.api.files import files_router

files_app_router = APIRouter()
files_app_router.include_router(files_router)
