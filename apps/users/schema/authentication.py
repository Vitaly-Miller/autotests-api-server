from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, UUID4

from utils.schema.database import DatabaseSchema


class Token(DatabaseSchema):
    token_type: str = Field(alias="tokenType", default="bearer")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class TokenData(DatabaseSchema):
    expire: datetime = Field(default_factory=datetime.now)
    user_id: UUID4


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: Token


class RefreshRequest(BaseModel):
    refresh_token: str = Field(alias="refreshToken")
