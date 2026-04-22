import uuid

from fastapi import HTTPException, status

from apps.exercises.schema.exercises import GetExerciseResponse, Exercise, GetExercisesQuery, GetExercisesResponse, \
    CreateExerciseRequest, UpdateExerciseRequest
from services.database.repositories.exercises import ExercisesRepository


async def get_exercise(
        exercise_id: uuid.UUID,
        exercises_repository: ExercisesRepository
) -> GetExerciseResponse:
    exercise = await exercises_repository.get_by_id(exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )

    return GetExerciseResponse(exercise=Exercise.model_validate(exercise))


async def get_exercises(
        query: GetExercisesQuery,
        exercises_repository: ExercisesRepository
) -> GetExercisesResponse:
    exercises = await exercises_repository.filter(query.course_id)

    return GetExercisesResponse(
        exercises=[Exercise.model_validate(exercise) for exercise in exercises]
    )


async def create_exercise(
        request: CreateExerciseRequest,
        exercises_repository: ExercisesRepository
) -> GetExerciseResponse:
    exercise = await exercises_repository.create(request.model_dump())

    return GetExerciseResponse(exercise=Exercise.model_validate(exercise))


async def update_exercise(
        exercise_id: uuid.UUID,
        request: UpdateExerciseRequest,
        exercises_repository: ExercisesRepository
) -> GetExerciseResponse:
    exercise = await exercises_repository.update(exercise_id, request.model_dump(exclude_unset=True))

    return GetExerciseResponse(exercise=Exercise.model_validate(exercise))


async def delete_exercise(exercise_id: uuid.UUID, exercises_repository: ExercisesRepository):
    await exercises_repository.delete(exercise_id)
