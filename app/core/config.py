from pydantic_settings import BaseSettings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    postgresql_url: str
    secret_key: str
    refresh_secret_key: str
    hash_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config:
        env_file = str(PROJECT_ROOT / ".env")

settings = Settings()

