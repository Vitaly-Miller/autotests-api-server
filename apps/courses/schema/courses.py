from typing import Self

from fastapi import Query
from pydantic import UUID4, Field, BaseModel, model_validator

from apps.files.schema.files import File
from apps.users.schema.users import User
from utils.schema.database import DatabaseSchema
from utils.schema.query import QuerySchema


class Course(DatabaseSchema):
    id: UUID4
    title: str = Field(min_length=1, max_length=250)
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    description: str = Field(min_length=1)
    preview_file: File = Field(alias="previewFile")
    estimated_time: str | None = Field(alias="estimatedTime", default=None, min_length=1, max_length=50)
    created_by_user: User = Field(alias="createdByUser")


class CreateCourseRequest(BaseModel):
    title: str = Field(min_length=1, max_length=250)
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    description: str = Field(min_length=1)
    estimated_time: str | None = Field(alias="estimatedTime", default=None, min_length=1, max_length=50)
    preview_file_id: UUID4 = Field(alias="previewFileId")
    created_by_user_id: UUID4 = Field(alias="createdByUserId")

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if (self.max_score or 0) < (self.min_score or 0):
            raise ValueError('max score should not be less than min score')

        return self


class UpdateCourseRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=250)
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    description: str | None = Field(default=None, min_length=1)
    estimated_time: str | None = Field(alias="estimatedTime", default=None, min_length=1, max_length=50)

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if (self.max_score is None) or (self.min_score is None):
            return self

        if self.max_score < self.min_score:
            raise ValueError('max score should not be less than min score')

        return self


class GetCoursesQuery(QuerySchema):
    user_id: UUID4 = Field(alias="userId")

    @classmethod
    async def as_query(cls, user_id: UUID4 = Query(alias="userId")) -> Self:
        return GetCoursesQuery(user_id=user_id)


class GetCourseResponse(BaseModel):
    course: Course


class GetCoursesResponse(BaseModel):
    courses: list[Course]
