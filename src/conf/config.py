# from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseSettings
#
# from pydantic import (
#     AliasChoices,
#     AmqpDsn,
#     BaseModel,
#     Field,
#     ImportString,
#     PostgresDsn,
#     RedisDsn,
# )


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_prefix='')
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@localhost:5432/postgres'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    mail_username: str = 'example@meta.ua'
    mail_password: str = 'password'
    mail_from: str = 'example@meta.ua'
    mail_port: int = 465
    mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = 'password'
    openai_api_key: str = 'key'
    # cloudinary_name: str = 'name'
    # cloudinary_api_key: str = 1234567890
    # cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
