"""
Session service provider for NOVA system integration.

This module provides dependency injection for session service instances,
configured with NOVA system settings.
"""

from typing import Annotated

from fastapi import Depends

from organization_server_demo.modules.nova.providers.settings_provider import get_settings
from organization_server_demo.modules.nova.services.session_service import SessionService
from organization_server_demo.settings import NovaSettings


async def get_session_service(settings: Annotated[NovaSettings, Depends(get_settings)]) -> SessionService:
    """
    Dependency provider for session service instances.
    
    Creates and returns a SessionService instance configured with the NOVA system
    API credentials and base URL from the application settings.
    
    Args:
        settings: NOVA system settings containing API credentials.
        
    Returns:
        SessionService: Configured session service instance.
    """
    api_key = settings.api_key
    base_url = settings.base_url
    return SessionService(base_url, api_key)