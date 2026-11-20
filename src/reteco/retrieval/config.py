"""
Centralized configuration for retrieval module.
Use pydantic-settings for validation and management of configuration values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Settings for the retrieval module.
    """

    # Add your configuration variables here
    # Example:
    # database_url: str = "sqlite:///./test.db"
    # api_key: str = "your_api_key"
    env: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def is_production(self) -> bool:
        """
        Check if the application is running in production mode.
        """
        return self.env == "production"

@lru_cache()
def get_settings() -> Settings:
    """
    Get the settings instance with caching to avoid reloading.
    """
    return Settings()