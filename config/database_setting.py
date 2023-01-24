from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = "./.env"


database_settings = DatabaseSettings()
