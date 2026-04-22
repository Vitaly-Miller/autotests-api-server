from fastapi import APIRouter

from apps.exercises.api.exercises import exercises_router

exercises_app_router = APIRouter()
exercises_app_router.include_router(exercises_router)
