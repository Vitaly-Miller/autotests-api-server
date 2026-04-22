import uuid

from fastapi import UploadFile, HTTPException, status

from apps.files.schema.files import CreateFileRequest, GetFileResponse, File
from services.database.repositories.files import FilesRepository


async def get_file(file_id: uuid.UUID, files_repository: FilesRepository) -> GetFileResponse:
    database_file = await files_repository.get_by_id(file_id)
    if not database_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return GetFileResponse(file=File.model_validate(database_file))


async def create_file(
        request: CreateFileRequest,
        upload_file: UploadFile,
        files_repository: FilesRepository
) -> GetFileResponse:
    database_file = await files_repository.create(request.model_dump())

    database_file.system_directory.mkdir(exist_ok=True)
    database_file.system_file.touch(exist_ok=True)
    database_file.system_file.write_bytes(await upload_file.read())

    return GetFileResponse(file=File.model_validate(database_file))


async def delete_file(file_id: uuid.UUID, files_repository: FilesRepository):
    database_file = await files_repository.get_by_id(file_id)
    if not database_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    database_file.system_file.unlink(missing_ok=True)
    await files_repository.delete(file_id)
