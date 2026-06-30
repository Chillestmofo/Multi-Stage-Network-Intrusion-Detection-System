"""
Simple token-based authentication middleware for IDS API
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os

# Load API token from environment or use default (CHANGE IN PRODUCTION!)
API_TOKEN = os.getenv("IDS_API_TOKEN", "your-secure-token-here-change-in-production")

security = HTTPBearer(auto_error=False)

def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> bool:
    """
    Verify the bearer token from request headers.
    Usage: add as dependency to protected routes
    
    Example:
        @app.post("/report", dependencies=[Depends(verify_token)])
        def report_detection(detection: dict):
            ...
    """
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return True

def optional_verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> bool:
    """
    Optional token verification (for public endpoints that can be secured)
    Returns True if valid token, False if no token, raises on invalid token
    """
    if credentials is None:
        return False
    
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return True
