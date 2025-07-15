"""
NOVA system settings model.

This module defines the configuration model for NOVA system integration,
including API credentials and device action configuration.
"""

from pydantic import BaseModel, AnyHttpUrl


class NovaSettings(BaseModel):
    """
    Configuration settings for NOVA system integration.
    
    Contains the necessary configuration for connecting to and interacting
    with the NOVA system API.
    
    Attributes:
        api_key: API key for authenticating with the NOVA system.
        base_url: Base URL for the NOVA system API.
        enabled_device_action_ids: List of device action IDs that are enabled.
    """
    api_key: str
    base_url: AnyHttpUrl
    enabled_device_action_ids: list[str] = []
