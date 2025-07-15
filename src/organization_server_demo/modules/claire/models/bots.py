"""
Bot-related data models for Claire integration.

This module defines the data models for bot entities, including bot definitions
and identifiers used in the Claire ecosystem.
"""

from typing import NewType, Any

from pydantic import BaseModel

from organization_server_demo.modules.base.prefixed_id import PrefixedUUID

BotID = NewType("BotID", PrefixedUUID("bot"))


class BotDefinition(BaseModel):
    """
    Definition of a bot entity.
    
    Represents a bot available in the Claire with its configuration
    and metadata.
    
    Attributes:
        name: Human-readable name of the bot.
        bot_id: Unique identifier for the bot with 'bot' prefix.
        meta: Additional metadata associated with the bot.
    """
    name: str
    bot_id: BotID
    meta: Any
