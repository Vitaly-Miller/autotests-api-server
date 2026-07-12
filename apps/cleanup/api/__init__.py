from fastapi import APIRouter

from apps.cleanup.api.cleanup import cleanup_router

cleanup_app_router = APIRouter()
cleanup_app_router.include_router(cleanup_router)
