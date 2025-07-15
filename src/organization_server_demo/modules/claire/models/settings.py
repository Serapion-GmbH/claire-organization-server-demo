"""
Claire settings model.

This module defines the configuration model for Claire ecosystem integration,
including API credentials and device action configuration.
"""

from pydantic import BaseModel, AnyHttpUrl


class ClaireSettings(BaseModel):
    """
    Configuration settings for Claire integration.
    
    Contains the necessary configuration for connecting to and interacting
    with the Claire API.
    
    Attributes:
        api_key: API key for authenticating with the Claire.
        base_url: Base URL for the Claire API.
        enabled_device_action_ids: List of device action IDs that are enabled.
    """
    api_key: str
    base_url: AnyHttpUrl
    enabled_device_action_ids: list[str] = []
