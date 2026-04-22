from typing import Self

from pydantic import DirectoryPath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='allow',
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='.',
    )

    app_host: HttpUrl

    database_url: str

    jwt_algorithm: str
    jwt_secret_key: str
    jwt_access_token_expire: int
    jwt_refresh_token_expire: int

    storage_directory: DirectoryPath

    @classmethod
    def init(cls) -> Self:
        storage_directory = DirectoryPath('./storage')
        storage_directory.mkdir(exist_ok=True)

        return Settings(storage_directory=storage_directory)


settings = Settings.init()
