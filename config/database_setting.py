from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    URI: str
    MONGO_DATABASE: str
    LOGS_COLLECTION: str

    class Config:
        env_file = "./.env"


database_settings = DatabaseSettings()
