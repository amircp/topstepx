"""TopStepX API Client"""

import httpx
from datetime import datetime
from typing import Optional

from .auth import TopStepXAuth
from .models import OrderType, OrderSide
from .exceptions import APIError, OrderError, PositionError


class TopStepXClient:
    """
    Client for interacting with TopStepX API.
    
    Example usage:
        auth = TopStepXAuth("username", "api_key")
        client = TopStepXClient(auth)
        
        accounts = await client.get_active_accounts()
        contracts = await client.get_available_contracts()
    """
    
    BASE_URL = "https://api.topstepx.com"

    def __init__(self, auth: TopStepXAuth):
        """
        Initialize the client.
        
        Args:
            auth: TopStepXAuth instance for authentication
        """
        self.auth = auth

    # ==================== Account Methods ====================

    async def get_active_accounts(self) -> list:
        """
        Get list of active accounts.
        
        Returns:
            List of active account dictionaries
            
        Raises:
            APIError: If the request fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Account/search",
                json={"onlyActiveAccounts": True},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("accounts", [])
            else:
                raise APIError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    # ==================== Contract Methods ====================

    async def get_available_contracts(self, live: bool = True) -> list:
        """
        Get list of available contracts.
        
        Args:
            live: If True, get live contracts; otherwise demo
            
        Returns:
            List of available contract dictionaries
            
        Raises:
            APIError: If the request fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Contract/available",
                json={"live": live},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("contracts", [])
            else:
                raise APIError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    # ==================== Order Methods ====================

    async def place_order(
        self,
        account_id: int,
        contract_id: str,
        order_type: OrderType,
        side: OrderSide,
        size: int,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        trail_price: Optional[float] = None,
        custom_tag: Optional[str] = None,
        linked_order_id: Optional[int] = None
    ) -> dict:
        """
        Place an order.
        
        Args:
            account_id: The account ID
            contract_id: The contract ID (e.g., "CON.F.US.EP.M25")
            order_type: Type of order (LIMIT, MARKET, STOP, etc.)
            side: Order side (BUY or SELL)
            size: Number of contracts
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders
            trail_price: Trail price for trailing stop orders
            custom_tag: Custom tag for the order
            linked_order_id: ID of linked order (for OCO orders)
            
        Returns:
            Order response dictionary
            
        Raises:
            OrderError: If the order fails
        """
        await self.auth.get_valid_token()

        order_data = {
            "accountId": account_id,
            "contractId": contract_id,
            "type": int(order_type),
            "side": int(side),
            "size": size,
            "limitPrice": limit_price,
            "stopPrice": stop_price,
            "trailPrice": trail_price,
            "customTag": custom_tag,
            "linkedOrderId": linked_order_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Order/place",
                json=order_data,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data
            else:
                raise OrderError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def search_orders(
        self,
        account_id: int,
        start_timestamp: datetime,
        end_timestamp: Optional[datetime] = None
    ) -> list:
        """
        Search for orders within a time range.
        
        Args:
            account_id: The account ID
            start_timestamp: Start of the time range
            end_timestamp: End of the time range (optional)
            
        Returns:
            List of order dictionaries
            
        Raises:
            OrderError: If the search fails
        """
        await self.auth.get_valid_token()

        payload = {
            "accountId": account_id,
            "startTimestamp": start_timestamp.isoformat(),
        }
        if end_timestamp:
            payload["endTimestamp"] = end_timestamp.isoformat()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Order/search",
                json=payload,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("orders", [])
            else:
                raise OrderError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def get_open_orders(self, account_id: int) -> list:
        """
        Get open orders for an account.
        
        Args:
            account_id: The account ID
            
        Returns:
            List of open order dictionaries
            
        Raises:
            OrderError: If the request fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Order/searchOpen",
                json={"accountId": account_id},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("orders", [])
            else:
                raise OrderError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def cancel_order(self, account_id: int, order_id: int) -> dict:
        """
        Cancel an order.
        
        Args:
            account_id: The account ID
            order_id: The order ID to cancel
            
        Returns:
            Response dictionary
            
        Raises:
            OrderError: If cancellation fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Order/cancel",
                json={"accountId": account_id, "orderId": order_id},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data
            else:
                raise OrderError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def modify_order(
        self,
        account_id: int,
        order_id: int,
        size: Optional[int] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        trail_price: Optional[float] = None
    ) -> dict:
        """
        Modify an open order.
        
        Args:
            account_id: The account ID
            order_id: The order ID to modify
            size: New size (optional)
            limit_price: New limit price (optional)
            stop_price: New stop price (optional)
            trail_price: New trail price (optional)
            
        Returns:
            Response dictionary
            
        Raises:
            OrderError: If modification fails
        """
        await self.auth.get_valid_token()

        payload = {
            "accountId": account_id,
            "orderId": order_id,
            "size": size,
            "limitPrice": limit_price,
            "stopPrice": stop_price,
            "trailPrice": trail_price
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Order/modify",
                json=payload,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data
            else:
                raise OrderError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    # ==================== Position Methods ====================

    async def get_open_positions(self, account_id: int) -> list:
        """
        Get open positions for an account.
        
        Args:
            account_id: The account ID
            
        Returns:
            List of open position dictionaries
            
        Raises:
            PositionError: If the request fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Position/searchOpen",
                json={"accountId": account_id},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("positions", [])
            else:
                raise PositionError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def close_position(self, account_id: int, contract_id: str) -> dict:
        """
        Close an entire position.
        
        Args:
            account_id: The account ID
            contract_id: The contract ID to close
            
        Returns:
            Response dictionary
            
        Raises:
            PositionError: If closing fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Position/closeContract",
                json={"accountId": account_id, "contractId": contract_id},
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data
            else:
                raise PositionError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    async def partial_close_position(
        self,
        account_id: int,
        contract_id: str,
        size: int
    ) -> dict:
        """
        Partially close a position.
        
        Args:
            account_id: The account ID
            contract_id: The contract ID
            size: Number of contracts to close
            
        Returns:
            Response dictionary
            
        Raises:
            PositionError: If partial close fails
        """
        await self.auth.get_valid_token()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Position/partialCloseContract",
                json={
                    "accountId": account_id,
                    "contractId": contract_id,
                    "size": size
                },
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data
            else:
                raise PositionError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )

    # ==================== Trade Methods ====================

    async def search_trades(
        self,
        account_id: int,
        start_timestamp: datetime,
        end_timestamp: Optional[datetime] = None
    ) -> list:
        """
        Search for trades within a time range.
        
        Args:
            account_id: The account ID
            start_timestamp: Start of the time range
            end_timestamp: End of the time range (optional)
            
        Returns:
            List of trade dictionaries. Note: profitAndLoss is null
            for half-turn trades (opening trades).
            
        Raises:
            APIError: If the search fails
        """
        await self.auth.get_valid_token()

        payload = {
            "accountId": account_id,
            "startTimestamp": start_timestamp.isoformat(),
        }
        if end_timestamp:
            payload["endTimestamp"] = end_timestamp.isoformat()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/api/Trade/search",
                json=payload,
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success") and data.get("errorCode") == 0:
                return data.get("trades", [])
            else:
                raise APIError(
                    message=data.get("errorMessage", "Unknown error"),
                    error_code=data.get("errorCode")
                )
