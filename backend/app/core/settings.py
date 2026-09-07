from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, EmailStr, PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_NAME: str = "OpsPilot"
    ADMIN_EMAIL: EmailStr = "dio@cortora.it"
    API_KEY: SecretStr = "rubbish here"
    DATABASE_URL: str
    APP_DOMAIN: str = "opspilot.com"

    CORS_ORIGINS: list[str] = ["Somethings", "other thing"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["Somethings", "other thing"]

    APP_VERSION: int = 1.0


settings = Settings()

## For the big apps, i know we could split the settings into
# different modules so that the codebase stays mantainable. For now, we keep all here
