from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    sqlalchemy_database_url: str = Field()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
