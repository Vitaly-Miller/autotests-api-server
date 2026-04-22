import uuid

from fastapi import HTTPException, status

from apps.courses.schema.courses import GetCoursesQuery, GetCoursesResponse, Course, CreateCourseRequest, \
    GetCourseResponse, UpdateCourseRequest
from apps.files.controllers.files import delete_file
from services.database.repositories.courses import CoursesRepository
from services.database.repositories.files import FilesRepository


async def get_course(
        course_id: uuid.UUID,
        courses_repository: CoursesRepository
) -> GetCourseResponse:
    course = await courses_repository.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )

    return GetCourseResponse(course=Course.model_validate(course))


async def get_courses(
        query: GetCoursesQuery,
        courses_repository: CoursesRepository
) -> GetCoursesResponse:
    courses = await courses_repository.filter(query.user_id)

    return GetCoursesResponse(courses=[Course.model_validate(course) for course in courses])


async def create_course(
        request: CreateCourseRequest,
        courses_repository: CoursesRepository
) -> GetCourseResponse:
    course = await courses_repository.create(request.model_dump())

    return GetCourseResponse(course=Course.model_validate(course))


async def update_course(
        course_id: uuid.UUID,
        request: UpdateCourseRequest,
        courses_repository: CoursesRepository
) -> GetCourseResponse:
    course = await courses_repository.update(course_id, request.model_dump(exclude_unset=True))

    return GetCourseResponse(course=Course.model_validate(course))


async def delete_course(
        course_id: uuid.UUID,
        files_repository: FilesRepository,
        courses_repository: CoursesRepository
):
    course = await courses_repository.get_by_id(course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
        )

    await delete_file(course.preview_file_id, files_repository)

    await courses_repository.delete(course_id)
