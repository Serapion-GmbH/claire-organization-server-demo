"""
Settings provider for Claire configuration.

This module provides dependency injection for accessing Claire settings
in FastAPI route handlers.
"""
from organization_server_demo.modules.claire.models.settings import ClaireSettings
from organization_server_demo.settings import SHARED_SETTINGS


async def get_settings() -> ClaireSettings:
    """
    Dependency provider for Claire settings.
    
    Returns the Claire configuration settings for use in FastAPI
    route handlers through dependency injection.
    
    Returns:
        ClaireSettings: The Claire configuration settings.
    """
    return SHARED_SETTINGS.claire
