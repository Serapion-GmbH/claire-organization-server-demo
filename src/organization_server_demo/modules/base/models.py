"""
Base data models for the organization server demo.

This module defines common data structures used throughout the application,
including pagination utilities and cursor-based result models.
"""

from typing import TypeVar, Generic

from pydantic import BaseModel

Item = TypeVar("Item", bound=BaseModel)


class Cursor(BaseModel):
    """
    Cursor for pagination operations.
    
    Attributes:
        cursor_id: String identifier for the cursor position.
    """
    cursor_id: str


class PaginatedResults(BaseModel, Generic[Item]):
    """
    Generic paginated results container.
    
    Provides a standardized way to return paginated data with cursor-based
    pagination support.
    
    Attributes:
        cursor: Optional cursor for retrieving next page of results.
        results: List of items for the current page.
    """
    cursor: Cursor | None
    results: list[Item]