"""
Settings provider for NOVA system configuration.

This module provides dependency injection for accessing NOVA system settings
in FastAPI route handlers.
"""

from organization_server_demo.modules.nova.models.settings import NovaSettings
from organization_server_demo.settings import SHARED_SETTINGS


async def get_settings() -> NovaSettings:
    """
    Dependency provider for NOVA system settings.
    
    Returns the NOVA system configuration settings for use in FastAPI
    route handlers through dependency injection.
    
    Returns:
        NovaSettings: The NOVA system configuration settings.
    """
    return SHARED_SETTINGS.nova
