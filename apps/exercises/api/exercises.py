import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from apps.exercises.controllers.exercises import get_exercises, get_exercise, delete_exercise, update_exercise, \
    create_exercise
from apps.exercises.schema.exercises import GetExercisesQuery, GetExercisesResponse, GetExerciseResponse, \
    CreateExerciseRequest, UpdateExerciseRequest
from apps.users.controllers.authentication import get_user_me
from services.database.repositories.exercises import ExercisesRepository, get_exercises_repository
from utils.routes import APIRoutes

exercises_router = APIRouter(
    prefix=APIRoutes.EXERCISES,
    tags=[APIRoutes.EXERCISES.as_tag()]
)


@exercises_router.get(
    '',
    dependencies=[Depends(get_user_me)],
    response_model=GetExercisesResponse
)
async def get_exercises_view(
        query: Annotated[GetExercisesQuery, Depends(GetExercisesQuery.as_query)],
        exercises_repository: Annotated[ExercisesRepository, Depends(get_exercises_repository)]
):
    return await get_exercises(query, exercises_repository)


@exercises_router.get(
    '/{exercise_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetExerciseResponse
)
async def get_exercise_view(
        exercise_id: uuid.UUID,
        exercises_repository: Annotated[ExercisesRepository, Depends(get_exercises_repository)]
):
    return await get_exercise(exercise_id, exercises_repository)


@exercises_router.post(
    '',
    dependencies=[Depends(get_user_me)],
    response_model=GetExerciseResponse
)
async def create_exercise_view(
        request: CreateExerciseRequest,
        exercises_repository: Annotated[ExercisesRepository, Depends(get_exercises_repository)]
):
    return await create_exercise(request, exercises_repository)


@exercises_router.patch(
    '/{exercise_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetExerciseResponse
)
async def update_exercise_view(
        exercise_id: uuid.UUID,
        request: UpdateExerciseRequest,
        exercises_repository: Annotated[ExercisesRepository, Depends(get_exercises_repository)]
):
    return await update_exercise(exercise_id, request, exercises_repository)


@exercises_router.delete('/{exercise_id}', dependencies=[Depends(get_user_me)])
async def delete_exercise_view(
        exercise_id: uuid.UUID,
        exercises_repository: Annotated[ExercisesRepository, Depends(get_exercises_repository)]
):
    return await delete_exercise(exercise_id, exercises_repository)
