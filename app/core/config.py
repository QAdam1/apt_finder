"""Application configuration using Pydantic settings."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings loaded from environment variables or .env file."""

    mongo_uri: str = Field(..., alias="MONGO_URI")
    mongo_db_name: str = Field(..., alias="MONGO_DB_NAME")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


def get_settings() -> Settings:
    """Return a singleton settings instance."""
    # In a larger app we might cache this, but for simplicity we instantiate directly.
    return Settings()


settings = get_settings()
