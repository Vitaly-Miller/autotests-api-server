import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from apps.courses.controllers.courses import get_courses, create_course, update_course, get_course, delete_course
from apps.courses.schema.courses import GetCoursesQuery, GetCoursesResponse, CreateCourseRequest, GetCourseResponse, \
    UpdateCourseRequest
from apps.users.controllers.authentication import get_user_me
from services.database.repositories.courses import CoursesRepository, get_courses_repository
from services.database.repositories.files import FilesRepository, get_files_repository
from utils.routes import APIRoutes

courses_router = APIRouter(
    prefix=APIRoutes.COURSES,
    tags=[APIRoutes.COURSES.as_tag()]
)


@courses_router.get(
    '',
    dependencies=[Depends(get_user_me)],
    response_model=GetCoursesResponse
)
async def get_courses_view(
        query: Annotated[GetCoursesQuery, Depends(GetCoursesQuery.as_query)],
        courses_repository: Annotated[CoursesRepository, Depends(get_courses_repository)]
):
    return await get_courses(query, courses_repository)


@courses_router.get(
    '/{course_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetCourseResponse
)
async def get_course_view(
        course_id: uuid.UUID,
        courses_repository: Annotated[CoursesRepository, Depends(get_courses_repository)]
):
    return await get_course(course_id, courses_repository)


@courses_router.post(
    '',
    dependencies=[Depends(get_user_me)],
    response_model=GetCourseResponse
)
async def create_course_view(
        request: CreateCourseRequest,
        courses_repository: Annotated[CoursesRepository, Depends(get_courses_repository)]
):
    return await create_course(request, courses_repository)


@courses_router.patch(
    '/{course_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetCourseResponse
)
async def update_course_view(
        course_id: uuid.UUID,
        request: UpdateCourseRequest,
        courses_repository: Annotated[CoursesRepository, Depends(get_courses_repository)]
):
    return await update_course(course_id, request, courses_repository)


@courses_router.delete('/{course_id}', dependencies=[Depends(get_user_me)])
async def delete_course_view(
        course_id: uuid.UUID,
        files_repository: Annotated[FilesRepository, Depends(get_files_repository)],
        courses_repository: Annotated[CoursesRepository, Depends(get_courses_repository)]
):
    return await delete_course(
        course_id,
        files_repository=files_repository,
        courses_repository=courses_repository
    )
