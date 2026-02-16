from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER : str
    POSTGRES_PORT : int
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_DB : str

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_ignore_empty=True,
        extra="ignore"
    )

    @property
    def POSTGRES_URL(self):
        return f"postgres+asyncg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = DatabaseSettings()


print(settings.POSTGRES_DB)
print(settings.POSTGRES_PASSWORD)