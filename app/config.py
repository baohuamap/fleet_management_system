## setting for db
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    redis_server: str
    redis_port: int

    class Config:
        env_file = "app.env"


settings = Settings()
