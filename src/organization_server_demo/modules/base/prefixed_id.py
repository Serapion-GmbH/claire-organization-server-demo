"""
Prefixed UUID utilities for Pydantic models.

This module provides utilities for creating UUID types with string prefixes
for use in Pydantic models, including validation and serialization.
"""

import re
from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator, PlainSerializer, Field
from pydantic_core.core_schema import SerializationInfo


def prefixed_uuid_validator(prefix: str):
    """
    Create a validator function for prefixed UUIDs.
    
    Args:
        prefix: The string prefix to expect before the UUID.
        
    Returns:
        BeforeValidator: A Pydantic validator that validates prefixed UUID strings.
    """
    uuid_pattern = re.compile(
        rf"^{re.escape(prefix)}-([a-f0-9]{{8}}-[a-f0-9]{{4}}-[a-f0-9]{{4}}-[a-f0-9]{{4}}-[a-f0-9]{{12}})$",
        re.IGNORECASE,
    )

    def validate_prefixed_uuid(value: UUID | str) -> UUID:
        """
        Validate and extract UUID from prefixed string.
        
        Args:
            value: Input value to validate (UUID or string).
            
        Returns:
            UUID: The extracted UUID object.
            
        Raises:
            ValueError: If the value is not a valid prefixed UUID.
        """
        if isinstance(value, UUID):
            return value
        if not isinstance(value, str):
            raise ValueError("Value must be a string or UUID")
        match = uuid_pattern.match(value)
        if not match:
            raise ValueError(f"Value must be a UUID with prefix {prefix}")
        return UUID(match.group(1))

    return BeforeValidator(validate_prefixed_uuid)


def prefixed_uuid_serializer(prefix: str):
    """
    Create a serializer function for prefixed UUIDs.
    
    Args:
        prefix: The string prefix to add when serializing.
        
    Returns:
        PlainSerializer: A Pydantic serializer that adds prefix to UUIDs.
    """
    def serialize_prefixed_uuid(value: UUID, info: SerializationInfo) -> str | UUID:
        """
        Serialize UUID with prefix for JSON output.
        
        Args:
            value: UUID to serialize.
            info: Serialization context information.
            
        Returns:
            str | UUID: Prefixed string for JSON, UUID object otherwise.
        """
        if info.mode == "json":
            return f"{prefix}-{value}"
        return value

    return PlainSerializer(serialize_prefixed_uuid)


# noinspection PyPep8Naming
def PrefixedUUID(prefix: str) -> type[UUID]:
    """
    Create a Pydantic-compatible prefixed UUID type.
    
    This function creates a UUID type that expects a string prefix when parsing
    from strings and adds the prefix when serializing to JSON.
    
    Args:
        prefix: The string prefix to use for this UUID type.
        
    Returns:
        type[UUID]: An annotated UUID type with prefix validation and serialization.
    """
    return Annotated[
        Annotated[
            Annotated[
                UUID | str,
                Field(
                    json_schema_extra={
                        "anyOf": [{"type": "string"}],
                        "format": None,
                        "pattern": f"^{re.escape(prefix)}-"
                        r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})$",
                    }
                ),
            ],
            prefixed_uuid_validator(prefix),
        ],
        prefixed_uuid_serializer(prefix),
    ]
