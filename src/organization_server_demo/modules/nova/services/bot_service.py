"""
Bot service for NOVA system integration.

This module provides service layer functionality for managing bots,
including retrieving bot definitions from the NOVA system.
"""

import logging

from starlette import status

from organization_server_demo.modules.base.exceptions import OrganizationServerException
from organization_server_demo.modules.nova.models.bots import BotDefinition
from organization_server_demo.modules.nova.services.nova_service import NOVAService

logger = logging.getLogger(__name__)


class BotService(NOVAService):
    """
    Service class for bot management operations.
    
    Provides methods for interacting with bot-related endpoints in the NOVA system,
    including retrieving available bot definitions.
    """
    
    async def get_bots(self) -> list[BotDefinition]:
        """
        Retrieve all available bot definitions from the NOVA system.
        
        Makes an API call to the NOVA system to fetch the list of available bots
        and returns them as BotDefinition objects.
        
        Returns:
            list[BotDefinition]: List of available bot definitions.
            
        Raises:
            OrganizationServerException: If the API call fails or returns an error.
        """
        async with self._client as client:
            async with client.get("/m2m/organizations/bots") as resp:
                result = await resp.json()
                if resp.status != 200:
                    logger.error("Could not get bots. %s", result)
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not get bots."}
                    )
        return [BotDefinition.model_validate(bot) for bot in result]
