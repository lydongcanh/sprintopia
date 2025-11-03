"""
Authentication middleware for Supabase JWT token verification.
"""

import jwt
import logging
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Dict, Any

logger = logging.getLogger(__name__)


class AuthMiddleware:
    """Middleware to handle JWT authentication for Supabase tokens."""
    
    def __init__(self):
        self.jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
        if not self.jwt_secret:
            logger.warning("SUPABASE_JWT_SECRET environment variable not set")
    
    @property
    def public_paths(self) -> set[str]:
        """Paths that don't require authentication."""
        return {"/", "/health", "/docs", "/redoc", "/openapi.json"}
    
    async def __call__(self, request: Request, call_next):
        """Process the request through authentication middleware."""
        
        # Skip authentication for public endpoints
        if request.url.path in self.public_paths:
            response = await call_next(request)
            return response
        
        # Skip authentication for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response
        
        # Verify authorization header
        auth_result = self._verify_authorization_header(request)
        if isinstance(auth_result, JSONResponse):
            return auth_result
        
        # Verify JWT token
        token_result = self._verify_jwt_token(auth_result)
        if isinstance(token_result, JSONResponse):
            return token_result
        
        # Add user info to request state
        request.state.user = self._extract_user_info(token_result)
        
        logger.info(f"Authenticated user: {request.state.user['email']} ({request.state.user['sub']})")
        
        # Continue to the endpoint
        response = await call_next(request)
        return response
    
    def _verify_authorization_header(self, request: Request) -> str | JSONResponse:
        """Extract and verify the authorization header."""
        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header required"}
            )
        
        # Extract token from "Bearer <token>"
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise ValueError("Invalid authorization scheme")
            return token
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header format. Use 'Bearer <token>'"}
            )
    
    def _verify_jwt_token(self, token: str) -> Dict[str, Any] | JSONResponse:
        """Verify and decode the JWT token."""
        try:
            if not self.jwt_secret:
                logger.error("SUPABASE_JWT_SECRET environment variable not set")
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Server configuration error"}
                )
            
            # Decode and verify the JWT token
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=["HS256"],
                audience="authenticated"
            )
            return payload
            
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Token verification failed"}
            )
    
    def _extract_user_info(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant user information from JWT payload."""
        return {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "internal_user_id": payload.get("user_metadata", {}).get("internal_user_id"),
            "full_name": payload.get("user_metadata", {}).get("full_name"),
            "session_id": payload.get("session_id")
        }