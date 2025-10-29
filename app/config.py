from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    postgresql_url: str

    class Config:
        env_file = str(PROJECT_ROOT / ".env")

settings = Settings()

