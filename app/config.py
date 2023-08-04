## setting for db
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str = Field(default=...)
    database_port: str = Field(default=...)
    database_name: str = Field(default=...)
    database_username: str = Field(default=...)
    database_password: str = Field(default=...)

    secret_key: str = Field(default=...)
    algorithm: str = Field(default=...)
    access_token_expire_minutes: int = Field(default=...)

    redis_server: str = Field(default=...)
    redis_port: int = Field(default=...)

    model_config = SettingsConfigDict(env_file="app.env")

    # class Config:
    #     env_file = "app.env"


settings = Settings()
