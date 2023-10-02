from pydantic import BaseSettings


class Settings(BaseSettings):
    data_folder: str = 'name'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()