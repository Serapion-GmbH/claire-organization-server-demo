"""
Bot management router for NOVA system integration.

This module provides API endpoints for managing and retrieving bot information
in the organization server demo.
"""

from typing import Annotated, List

from fastapi import APIRouter, Depends

from organization_server_demo.modules.base.authenticated_user_provider import get_authenticated_user
from organization_server_demo.modules.nova.models.bots import BotDefinition
from organization_server_demo.modules.nova.providers.bot_provider import get_bot_service
from organization_server_demo.modules.nova.services.bot_service import BotService

router = APIRouter(tags=["Bots"])


@router.get("", response_model=List[BotDefinition], dependencies=[Depends(get_authenticated_user)])
async def get_bots(
    bot_service: Annotated[BotService, Depends(get_bot_service)],
):
    """
    Retrieve all available bots.
    
    Returns a list of all bot definitions available in the NOVA system.
    Requires authentication.
    
    Args:
        bot_service: Bot service dependency for retrieving bot data.
        
    Returns:
        List[BotDefinition]: List of available bot definitions.
    """
    return bot_service.get_bots()
