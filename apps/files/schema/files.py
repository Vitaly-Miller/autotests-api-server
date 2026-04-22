from pydantic import BaseModel, UUID4, computed_field, HttpUrl, Field

from config import settings
from utils.schema.database import DatabaseSchema


class File(DatabaseSchema):
    id: UUID4
    filename: str = Field(max_length=250)
    directory: str = Field(max_length=250)

    @computed_field
    def url(self) -> HttpUrl:
        return HttpUrl(f'{settings.app_host}static/{self.directory}/{self.filename}')


class CreateFileRequest(BaseModel):
    filename: str
    directory: str


class GetFileResponse(BaseModel):
    file: File
