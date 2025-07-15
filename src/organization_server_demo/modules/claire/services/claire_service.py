"""
Base service class for Claire integration.

This module provides the base service class that other Claire services inherit from,
containing common functionality for API communication.
"""

import aiohttp
from pydantic import AnyHttpUrl


class ClaireService:
    """
    Base service class for Claire API interactions.
    
    Provides common functionality for making authenticated HTTP requests to the
    Claire API, including automatic bearer token authentication.
    
    Attributes:
        _client: Configured aiohttp ClientSession for API requests.
    """
    
    def __init__(self, base_url: AnyHttpUrl, api_key: str):
        """
        Initialize the Claire service with API credentials.
        
        Sets up an aiohttp ClientSession with the Claire base URL and
        authorization headers for API communication.
        
        Args:
            base_url: Base URL for the Claire API.
            api_key: API key for authentication with the Claire.
        """
        self._client = aiohttp.ClientSession(
            base_url=str(base_url),
            headers={
                "Authorization": f"Bearer {api_key}",
            },
        )
