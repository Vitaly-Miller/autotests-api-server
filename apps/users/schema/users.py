from pydantic import UUID4, EmailStr, BaseModel, Field

from utils.schema.database import DatabaseSchema


class User(DatabaseSchema):
    id: UUID4
    email: EmailStr = Field(min_length=1, max_length=250)
    last_name: str = Field(alias="lastName", min_length=1, max_length=50)
    first_name: str = Field(alias="firstName", min_length=1, max_length=50)
    middle_name: str = Field(alias="middleName", min_length=1, max_length=50)


class CreateUserRequest(BaseModel):
    email: EmailStr = Field(min_length=1, max_length=250)
    password: str = Field(min_length=1, max_length=250)
    last_name: str = Field(alias="lastName", min_length=1, max_length=50)
    first_name: str = Field(alias="firstName", min_length=1, max_length=50)
    middle_name: str = Field(alias="middleName", min_length=1, max_length=50)


class UpdateUserRequest(BaseModel):
    email: EmailStr | None = Field(default=None, min_length=1, max_length=250)
    last_name: str | None = Field(alias="lastName", default=None, min_length=1, max_length=50)
    first_name: str | None = Field(alias="firstName", default=None, min_length=1, max_length=50)
    middle_name: str | None = Field(alias="middleName", default=None, min_length=1, max_length=50)


class GetUserResponse(BaseModel):
    user: User
