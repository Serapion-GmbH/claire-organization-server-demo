"""
Utility functions for the base module.

This module provides helper functions for working with prefixed IDs and other
common operations in the organization server demo.
"""

from typing import TypeVar, NewType

from pydantic import TypeAdapter

T = TypeVar("T", bound=NewType)


def dump_prefixed_id(prefixed_id_type: type[T], prefixed_id: T):
    """
    Serialize a prefixed ID to its string representation.
    
    Uses Pydantic's TypeAdapter to convert a prefixed ID to its JSON string format,
    which includes the prefix.
    
    Args:
        prefixed_id_type: The type of the prefixed ID.
        prefixed_id: The prefixed ID instance to serialize.
        
    Returns:
        str: The string representation of the prefixed ID.
    """
    return TypeAdapter(prefixed_id_type).dump_python(prefixed_id, mode="json")
