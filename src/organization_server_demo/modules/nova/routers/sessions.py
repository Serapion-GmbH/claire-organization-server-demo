"""
Session management router for NOVA system integration.

This module provides API endpoints for managing chat sessions, including
creation, listing, renewal, and deletion of sessions.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_auth0 import Auth0User

from organization_server_demo.modules.base.authenticated_user_provider import get_authenticated_user
from organization_server_demo.modules.base.models import PaginatedResults
from organization_server_demo.modules.base.utils import dump_prefixed_id
from organization_server_demo.modules.nova.models.bots import BotID
from organization_server_demo.modules.nova.models.sessions import ClientSessionResponse, SessionRequest, \
    MessageEditability, SessionRequestUser, ChatSessionDTO
from organization_server_demo.modules.nova.models.settings import NovaSettings
from organization_server_demo.modules.nova.providers.bot_provider import get_bot_service
from organization_server_demo.modules.nova.providers.session_provider import get_session_service
from organization_server_demo.modules.nova.providers.settings_provider import get_settings
from organization_server_demo.modules.nova.services.bot_service import BotService
from organization_server_demo.modules.nova.services.session_service import SessionService

router = APIRouter(tags=["Sessions"])


@router.post("", response_model=ClientSessionResponse)
async def create_session(
    bot_id: BotID,
    user: Annotated[Auth0User, Depends(get_authenticated_user)],
    settings: Annotated[NovaSettings, Depends(get_settings)],
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    """
    Create a new chat session.
    
    Creates a new session for the authenticated user with the specified bot
    and enabled device actions from the configuration.
    
    Args:
        bot_id: Identifier of the bot to use for the session.
        user: Authenticated user creating the session.
        settings: NOVA system settings containing enabled device actions.
        session_service: Session service dependency for session management.
        
    Returns:
        ClientSessionResponse: Session information and authentication token.
    """
    enabled_device_actions = settings.enabled_device_action_ids

    response = await session_service.create_session(
        SessionRequest(
            user=SessionRequestUser(organization_user_id=user.id),
            enabled_device_actions=enabled_device_actions,
            bot_id=bot_id,
            editable=MessageEditability.all_messages,
        )
    )
    return response


@router.get("", response_model=PaginatedResults[ChatSessionDTO])
async def list_sessions(
    session_service: Annotated[SessionService, Depends(get_session_service)],
    bot_service: Annotated[BotService, Depends(get_bot_service)],
    user: Annotated[Auth0User, Depends(get_authenticated_user)],
    cursor: str | None = None,
):
    """
    List sessions for the authenticated user.
    
    Retrieves a paginated list of chat sessions for the authenticated user,
    filtered by available bots.
    
    Args:
        session_service: Session service dependency for session management.
        bot_service: Bot service dependency for retrieving available bots.
        user: Authenticated user requesting their sessions.
        cursor: Optional cursor for pagination.
        
    Returns:
        PaginatedResults[ChatSessionDTO]: Paginated list of user sessions.
    """
    available_bots = [bot.bot_id for bot in await bot_service.get_bots()]

    response = await session_service.list_sessions(
        auth0_user_id=user.id, bot_ids=available_bots, cursor=cursor
    )
    return response


@router.post("/{session_id}/renew", response_model=ClientSessionResponse)
async def renew_session(
    session_id: str,
    user: Annotated[Auth0User, Depends(get_authenticated_user)],
    nova_service: Annotated[SessionService, Depends(get_session_service)],
):
    """
    Renew an existing session.
    
    Renews the authentication token for an existing session, allowing
    continued access to the session.
    
    Args:
        session_id: Identifier of the session to renew.
        user: Authenticated user renewing the session.
        nova_service: Session service dependency for session management.
        
    Returns:
        ClientSessionResponse: Updated session information and new token.
    """
    response = await nova_service.renew_session(session_id, user.id)

    return response


@router.delete("/{session_id}", dependencies=[Depends(get_authenticated_user)])
async def delete_session(
    session_id: str,
    nova_service: Annotated[SessionService, Depends(get_session_service)],
):
    """
    Delete a session.
    
    Permanently deletes a chat session. Requires authentication.
    
    Args:
        session_id: Identifier of the session to delete.
        nova_service: Session service dependency for session management.
        
    Returns:
        dict: Empty response object.
    """
    await nova_service.delete_session(session_id)
    return {}
