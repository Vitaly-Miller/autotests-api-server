import uuid
from pathlib import Path

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import Mapped

from config import settings
from utils.clients.database.mixin_model import MixinModel


class FilesModel(MixinModel):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    filename: Mapped[str] = Column(String(length=250), nullable=False)
    directory: Mapped[str] = Column(String(length=250), nullable=False)

    @property
    def system_file(self) -> Path:
        return settings.storage_directory.joinpath(self.directory, self.filename)

    @property
    def system_directory(self) -> Path:
        return settings.storage_directory.joinpath(self.directory)
