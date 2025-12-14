"""TopStepX Authentication Module"""

import httpx
from datetime import datetime, timedelta
from typing import Optional

from .exceptions import AuthenticationError


class TopStepXAuth:
    """Handles authentication with TopStepX API"""
    
    BASE_URL = "https://api.topstepx.com"
    TOKEN_VALIDITY_HOURS = 24
    TOKEN_REFRESH_MARGIN_MINUTES = 5

    def __init__(self, username: str, api_key: str):
        """
        Initialize authentication handler.
        
        Args:
            username: TopStepX username
            api_key: TopStepX API key
        """
        self.username = username
        self.api_key = api_key
        self.token: Optional[str] = None
        self.token_expires: Optional[datetime] = None

    async def get_valid_token(self) -> str:
        """
        Get a valid token, automatically renewing if necessary.
        
        Returns:
            Valid authentication token
            
        Raises:
            AuthenticationError: If login fails
        """
        if not self.token or self._is_token_expired():
            await self._login()
        return self.token

    def get_headers(self) -> dict:
        """
        Get headers with authorization token.
        
        Returns:
            Dictionary with Authorization header
        """
        return {"Authorization": f"Bearer {self.token}"}

    async def _login(self) -> None:
        """
        Perform login and obtain a new token.
        
        Raises:
            AuthenticationError: If login fails
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Auth/loginKey",
                json={
                    "userName": self.username,
                    "apiKey": self.api_key
                }
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                self.token = data["token"]
                self.token_expires = datetime.now() + timedelta(
                    hours=self.TOKEN_VALIDITY_HOURS
                )
            else:
                raise AuthenticationError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def validate_token(self) -> bool:
        """
        Validate if the current token is still valid.
        
        Returns:
            True if token is valid, False otherwise
        """
        if not self.token:
            return False

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Auth/validate",
                headers=self.get_headers()
            )
            return response.status_code == 200

    def _is_token_expired(self) -> bool:
        """
        Check if token has expired (with margin).
        
        Returns:
            True if token is expired or about to expire
        """
        if not self.token_expires:
            return True
        margin = timedelta(minutes=self.TOKEN_REFRESH_MARGIN_MINUTES)
        return datetime.now() >= (self.token_expires - margin)
