from fastapi import APIRouter

from apps.courses.api.courses import courses_router

courses_app_router = APIRouter()
courses_app_router.include_router(courses_router)
