import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Form

from apps.files.controllers.files import create_file, delete_file, get_file
from apps.files.schema.files import CreateFileRequest, GetFileResponse
from apps.users.controllers.authentication import get_user_me
from services.database.repositories.files import FilesRepository, get_files_repository
from utils.routes import APIRoutes

files_router = APIRouter(
    prefix=APIRoutes.FILES,
    tags=[APIRoutes.FILES.as_tag()]
)


@files_router.get(
    '/{file_id}',
    dependencies=[Depends(get_user_me)],
    response_model=GetFileResponse
)
async def get_file_view(
        file_id: uuid.UUID,
        files_repository: Annotated[FilesRepository, Depends(get_files_repository)]
):
    return await get_file(file_id, files_repository)


@files_router.post('', dependencies=[Depends(get_user_me)], response_model=GetFileResponse)
async def create_file_view(
        filename: Annotated[str, Form(min_length=1, max_length=255)],
        directory: Annotated[str, Form(min_length=1, max_length=1024)],
        upload_file: UploadFile,
        files_repository: Annotated[FilesRepository, Depends(get_files_repository)]
):
    request = CreateFileRequest(filename=filename, directory=directory)
    return await create_file(request, upload_file, files_repository)


@files_router.delete('/{file_id}', dependencies=[Depends(get_user_me)])
async def delete_file_view(
        file_id: uuid.UUID,
        files_repository: Annotated[FilesRepository, Depends(get_files_repository)]
):
    return await delete_file(file_id, files_repository)
