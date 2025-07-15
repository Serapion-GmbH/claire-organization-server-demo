"""
Session service for Claire integration.

This module provides service layer functionality for managing chat sessions,
including creation, listing, retrieval, renewal, and deletion operations.
"""

import json
import logging

from fastapi.encoders import jsonable_encoder
from starlette import status

from organization_server_demo.modules.base.exceptions import OrganizationServerException
from organization_server_demo.modules.base.models import PaginatedResults
from organization_server_demo.modules.base.utils import dump_prefixed_id
from organization_server_demo.modules.claire.models.bots import BotID
from organization_server_demo.modules.claire.models.sessions import SessionRequest, ClientSessionResponse, ChatSessionDTO
from organization_server_demo.modules.claire.services.claire_service import ClaireService

logger = logging.getLogger(__name__)


class SessionService(ClaireService):
    """
    Service class for session management operations.
    
    Provides methods for interacting with session-related endpoints in the Claire,
    including CRUD operations for chat sessions.
    """
    
    async def create_session(self, session_request: SessionRequest) -> ClientSessionResponse:
        """
        Create a new chat session in the Claire API.
        
        Sends a session creation request to the Claire API with the provided
        session parameters and returns the created session information.
        
        Args:
            session_request: Session creation request with user and bot information.
            
        Returns:
            ClientSessionResponse: Created session information and authentication token.
            
        Raises:
            OrganizationServerException: If the session creation fails.
        """
        encoded_body = json.dumps(session_request, default=jsonable_encoder).encode("utf-8")
        async with self._client as client:
            async with client.post(
                "/m2m/client_sessions",
                data=encoded_body,
                headers={
                    "Content-Type": "application/json",
                },
            ) as resp:
                result = await resp.json()
                if resp.status != 200:
                    logger.error("Could not create chat session: %s", result)
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not create chat session."}
                    )
        return ClientSessionResponse.model_validate(result)

    async def list_sessions(
        self, auth0_user_id: str, bot_ids: list[BotID], cursor: str | None
    ) -> PaginatedResults[ChatSessionDTO]:
        """
        List chat sessions for a specific user and bot IDs.
        
        Retrieves a paginated list of chat sessions filtered by user ID and
        available bot IDs.
        
        Args:
            auth0_user_id: External user ID from Auth0.
            bot_ids: List of bot IDs to filter sessions by.
            cursor: Optional cursor for pagination.
            
        Returns:
            PaginatedResults[ChatSessionDTO]: Paginated list of chat sessions.
            
        Raises:
            OrganizationServerException: If the session listing fails.
        """
        params = {
            "external_user_id": auth0_user_id,
            "bot_ids": [dump_prefixed_id(BotID, bot_id) for bot_id in bot_ids],
        }
        if cursor:
            params["cursor"] = cursor

        async with self._client as client:
            async with client.get("/m2m/client_sessions/", params=params) as resp:
                result = await resp.json()
                if resp.status != 200:
                    logger.error("Could not list chat sessions: %s", result)
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not list chat sessions."}
                    )
        return PaginatedResults[ChatSessionDTO].model_validate(result)

    async def get_session(self, session_id: str) -> ChatSessionDTO:
        """
        Retrieve a specific chat session by ID.
        
        Fetches detailed information about a chat session including messages
        and bot configuration.
        
        Args:
            session_id: Unique identifier of the session to retrieve.
            
        Returns:
            ChatSessionDTO: Detailed session information.
            
        Raises:
            OrganizationServerException: If the session retrieval fails.
        """
        async with self._client as client:
            async with client.get(f"/m2m/client_sessions/{session_id}") as resp:
                result = await resp.json()
                if resp.status != 200:
                    logger.error("Could not get chat session: %s", result)
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not get chat session."}
                    )
        return ChatSessionDTO.model_validate(result)

    async def delete_session(self, session_id: str):
        """
        Delete a chat session.
        
        Permanently removes a chat session from the Claire API.
        
        Args:
            session_id: Unique identifier of the session to delete.
            
        Raises:
            OrganizationServerException: If the session deletion fails.
        """
        async with self._client as client:
            async with client.delete(f"/m2m/client_sessions/{session_id}") as resp:
                if resp.status != 200:
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not delete chat session."}
                    )

    async def renew_session(self, session_id: str, external_user_id: str) -> ClientSessionResponse:
        """
        Renew an existing chat session.
        
        Refreshes the authentication token for an existing session, allowing
        continued access to the session.
        
        Args:
            session_id: Unique identifier of the session to renew.
            external_user_id: External user ID from Auth0.
            
        Returns:
            ClientSessionResponse: Renewed session information and new token.
            
        Raises:
            OrganizationServerException: If the session renewal fails.
        """
        body = {
            "external_user_id": external_user_id,
        }
        encoded_body = json.dumps(body, default=jsonable_encoder).encode("utf-8")

        async with self._client as client:
            async with client.post(
                f"/m2m/client_sessions/{session_id}/renew",
                data=encoded_body,
                headers={
                    "Content-Type": "application/json",
                },
            ) as resp:
                result = await resp.json()
                if resp.status != 200:
                    logger.error("Could not renew chat session: %s", result)
                    raise OrganizationServerException(
                        status_code=status.HTTP_502_BAD_GATEWAY, detail={"message": "Could not renew chat session."}
                    )
        return ClientSessionResponse.model_validate(result)
