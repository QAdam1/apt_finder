"""Shared configuration for services using Pydantic settings."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings loaded from environment variables or .env file."""

    mongo_uri: str = Field(..., alias="MONGO_URI")
    mongo_db_name: str = Field(..., alias="MONGO_DB_NAME")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")

    facebook_email: str | None = Field(None, alias="FACEBOOK_EMAIL")
    facebook_password: str | None = Field(None, alias="FACEBOOK_PASSWORD")
    facebook_group_id: str | None = Field(None, alias="FACEBOOK_GROUP_ID")
    facebook_pages: int = Field(1, alias="FACEBOOK_PAGES")
    facebook_request_kwargs: dict[str, object] = Field(default_factory=dict, alias="FACEBOOK_REQUEST_KWARGS")
    facebook_poll_interval_seconds: int = Field(900, alias="FACEBOOK_POLL_INTERVAL_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


def get_settings() -> Settings:
    """Return a singleton settings instance."""
    return Settings()


settings = get_settings()
