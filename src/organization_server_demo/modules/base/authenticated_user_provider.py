"""
User authentication provider for the organization server demo.

This module provides Auth0 integration for user authentication and authorization,
including dependency injection for authenticated user access.
"""

from typing import Annotated

from fastapi import Security
from fastapi_auth0 import Auth0User, Auth0
from starlette import status

from organization_server_demo.modules.base.exceptions import OrganizationServerException
from organization_server_demo.settings import SHARED_SETTINGS

auth_provider = Auth0(
    domain=SHARED_SETTINGS.auth0.domain,
    api_audience=SHARED_SETTINGS.auth0.audience,
    auto_error=True,
    scopes={},
)


async def get_authenticated_user(
    auth0_user: Annotated[Auth0User, Security(auth_provider.get_user, scopes=[])],
):
    """
    Dependency to get the authenticated user from Auth0.
    
    Validates that the user is properly authenticated and returns the Auth0User
    object for use in endpoint handlers.
    
    Args:
        auth0_user: Auth0User instance from the security dependency.
        
    Returns:
        Auth0User: The authenticated user object.
        
    Raises:
        OrganizationServerException: If the user is not authenticated.
    """
    if auth0_user is None:
        raise OrganizationServerException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authorized")

    return auth0_user