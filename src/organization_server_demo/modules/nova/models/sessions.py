"""
Session-related data models for NOVA system integration.

This module defines the data models for session management, including session
requests, responses, and chat session data transfer objects.
"""

import enum
from typing import NewType, Any

from pydantic import BaseModel

from organization_server_demo.modules.base.prefixed_id import PrefixedUUID
from organization_server_demo.modules.nova.models.bots import BotID

SessionID = NewType("SessionID", PrefixedUUID("session"))
OrganizationID = NewType("OrganizationID", PrefixedUUID("org"))


class SessionRequestUser(BaseModel):
    """
    User information for session requests.
    
    Attributes:
        organization_user_id: Unique identifier for the user within the organization.
    """
    organization_user_id: str


class MessageEditability(str, enum.Enum):
    """
    Enumeration of message editability levels.
    
    Defines the different levels of message editing permissions within a session.
    """
    none = "none"
    user_messages = "user_messages"
    all_messages = "all_messages"


class SessionRequest(BaseModel):
    """
    Request model for creating a new session.
    
    Contains all the necessary information to create a new chat session
    in the NOVA system.
    
    Attributes:
        user: User information for the session.
        bot_id: Identifier of the bot to use for the session.
        enabled_device_actions: List of device action IDs enabled for the session.
        editable: Message editability level for the session.
        meta: Additional metadata for the session.
    """
    user: SessionRequestUser
    bot_id: BotID
    enabled_device_actions: list[str]
    editable: MessageEditability = MessageEditability.none
    meta: Any = None


class SessionDto(BaseModel):
    """
    Data transfer object for session information.
    
    Represents a session with its core identifying information and configuration.
    
    Attributes:
        organization_id: Identifier of the organization owning the session.
        session_id: Unique identifier for the session.
        editable: Message editability level for the session.
        meta: Additional metadata for the session.
    """
    organization_id: OrganizationID
    session_id: SessionID
    editable: MessageEditability
    meta: Any = None


class ClientSessionResponse(BaseModel):
    """
    Response model for session creation and renewal.
    
    Contains session information and authentication token for client use.
    
    Attributes:
        session: Session data transfer object.
        token: Authentication token for the session.
    """
    session: SessionDto
    token: str


class ChatSessionDTO(BaseModel):
    """
    Data transfer object for chat session details.
    
    Represents a complete chat session with messages and bot configuration.
    
    Attributes:
        organization_id: Identifier of the organization owning the session.
        session_id: Unique identifier for the session.
        messages: List of messages in the session.
        bot_configuration: Configuration of the bot used in the session.
        meta: Additional metadata for the session.
    """
    organization_id: OrganizationID
    session_id: SessionID
    messages: list[Any]
    bot_configuration: Any
    meta: Any
