from pydantic import model_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore"
    )
    DAILY_LIKES_LIMIT: int = 10
    AVATARS_DIR: str = "app/static/avatars/"
    WATERMARK_PATH: str = "app/static/watermark.png"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "root"
    DB_NAME: str = "mydb"

    DATABASE_URL: str = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def assemble_database_url(cls, values):
        values["DATABASE_URL"] = (
            f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values

    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ENCRYPTION_KEY: str
    JWT_TOKEN_DELAY_MINUTES: int = 30
    ORIGINS: list = ["localhost:8000", "127.0.0.1:8000"]

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_PORT: int


settings = Settings()
