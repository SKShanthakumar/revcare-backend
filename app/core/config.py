from pydantic_settings import BaseSettings
from pydantic import BaseModel, ConfigDict
from bson import ObjectId
from pathlib import Path
from fastapi_mail import ConnectionConfig

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    postgresql_url: str
    secret_key: str
    refresh_secret_key: str
    hash_algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    razorpay_key_id: str
    razorpay_key_secret: str
    mongodb_uri: str
    mongodb_db: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str = "Revcare"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    template_folder: str = "app/templates/email"

    class Config:
        env_file = str(PROJECT_ROOT / ".env")

settings = Settings()

class BaseModelWithObjectId(BaseModel):
    model_config = ConfigDict(
        json_encoders={ObjectId: lambda v: str(v)},
    )

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
    TEMPLATE_FOLDER=settings.template_folder
)
