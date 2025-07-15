"""
Session service provider for Claire integration.

This module provides dependency injection for session service instances,
configured with Claire settings.
"""

from typing import Annotated

from fastapi import Depends

from organization_server_demo.modules.claire.models.settings import ClaireSettings
from organization_server_demo.modules.claire.providers.settings_provider import get_settings
from organization_server_demo.modules.claire.services.session_service import SessionService


async def get_session_service(settings: Annotated[ClaireSettings, Depends(get_settings)]) -> SessionService:
    """
    Dependency provider for session service instances.
    
    Creates and returns a SessionService instance configured with the Claire
    API credentials and base URL from the application settings.
    
    Args:
        settings: Claire settings containing API credentials.
        
    Returns:
        SessionService: Configured session service instance.
    """
    api_key = settings.api_key
    base_url = settings.base_url
    return SessionService(base_url, api_key)