"""
Application settings configuration.

This module defines the configuration classes for the organization server demo,
including CORS, Auth0, and NOVA system settings using Pydantic settings.
"""

from pydantic import field_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from organization_server_demo.modules.nova.models.settings import NovaSettings


class CORSSettings(BaseModel):
    """
    CORS (Cross-Origin Resource Sharing) configuration settings.
    
    Attributes:
        allowed_origins: List of allowed origins for CORS. Can be a string (comma-separated)
                        or list of strings, or None to disable CORS.
    """
    allowed_origins: list[str] | str | None = None

    @field_validator("allowed_origins")
    @classmethod
    def validate_allowed_origins(cls, allowed_origins: list[str] | str | None) -> list[str] | None:
        """
        Validate and normalize allowed origins.
        
        Args:
            allowed_origins: Raw allowed origins value from configuration.
            
        Returns:
            List of origin strings or None if not configured.
        """
        if allowed_origins is None:
            return None
        if isinstance(allowed_origins, str):
            return allowed_origins.split(",")
        return allowed_origins


class Auth0Settings(BaseModel):
    """
    Auth0 authentication configuration settings.
    
    Attributes:
        domain: Auth0 domain.
        audience: Auth0 API audience.
    """
    domain: str
    audience: str


class OrganizationServerSettings(BaseSettings):
    """
    Main application settings container.
    
    Combines all configuration settings for the organization server demo,
    including Auth0, NOVA, and CORS settings.
    
    Attributes:
        auth0: Auth0 authentication settings.
        nova: NOVA system integration settings.
        cors: CORS middleware settings.
    """
    auth0: Auth0Settings
    nova: NovaSettings
    cors: CORSSettings

    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            ".env.local"
        ],
        env_nested_delimiter="__",
        extra="ignore",
    )


SHARED_SETTINGS = OrganizationServerSettings()
