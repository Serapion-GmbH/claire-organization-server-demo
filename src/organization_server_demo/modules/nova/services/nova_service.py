"""
Base service class for NOVA system integration.

This module provides the base service class that other NOVA services inherit from,
containing common functionality for API communication.
"""

import aiohttp
from pydantic import AnyHttpUrl


class NOVAService:
    """
    Base service class for NOVA system API interactions.
    
    Provides common functionality for making authenticated HTTP requests to the
    NOVA system API, including automatic bearer token authentication.
    
    Attributes:
        _client: Configured aiohttp ClientSession for API requests.
    """
    
    def __init__(self, base_url: AnyHttpUrl, api_key: str):
        """
        Initialize the NOVA service with API credentials.
        
        Sets up an aiohttp ClientSession with the NOVA system base URL and
        authorization headers for API communication.
        
        Args:
            base_url: Base URL for the NOVA system API.
            api_key: API key for authentication with the NOVA system.
        """
        self._client = aiohttp.ClientSession(
            base_url=str(base_url),
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )
