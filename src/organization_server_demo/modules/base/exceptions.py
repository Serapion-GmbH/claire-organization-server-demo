"""
Custom exceptions for the organization server demo.

This module defines custom exception classes that extend FastAPI's HTTPException
to provide application-specific error handling.
"""

from fastapi import HTTPException


class OrganizationServerException(HTTPException):
    """
    Base exception for the organization server.
    
    Extends FastAPI's HTTPException to provide a common base for all
    organization server-specific exceptions.
    """