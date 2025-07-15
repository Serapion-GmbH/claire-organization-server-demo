"""
Bot service provider for Claire Ecosystem integration.

This module provides dependency injection for bot service instances,
configured with Claire settings.
"""

from typing import Annotated

from fastapi import Depends

from organization_server_demo.modules.claire.models.settings import ClaireSettings
from organization_server_demo.modules.claire.providers.settings_provider import get_settings
from organization_server_demo.modules.claire.services.bot_service import BotService


async def get_bot_service(settings: Annotated[ClaireSettings, Depends(get_settings)]) -> BotService:
    """
    Dependency provider for bot service instances.
    
    Creates and returns a BotService instance configured with the Claire
    API credentials and base URL from the application settings.
    
    Args:
        settings: Claire settings containing API credentials.
        
    Returns:
        BotService: Configured bot service instance.
    """
    api_key = settings.api_key
    base_url = settings.base_url
    return BotService(base_url, api_key)

