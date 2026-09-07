from pydantic_settings import BaseSettings, SettingsConfigDict, PostgresDsn
from pydantic import SecretStr, EmailStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_NAME: str = "OpsPilot"
    ADMIN_EMAIL: EmailStr = "dio@cortora.it"
    API_KEY: SecretStr
    DATABASE_URL: PostgresDsn
    APP_DOMAIN: str = "opspilot.com"

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    APP_VERSION: int = 1.0


settings = Settings()

## For the big apps, i know we could split the settings into
# different modules so that the codebase stays mantainable. For now, we keep all here
