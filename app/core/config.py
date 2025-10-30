from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    AVIATION_STACK_API_URL: str
    AVIATION_STACK_API_KEY: str

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    NOTIFICATION_EMAIL: str

    LOG_LEVEL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
