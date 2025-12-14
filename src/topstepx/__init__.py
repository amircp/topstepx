"""
TopStepX API Client Library

A Python client for interacting with the TopStepX trading API.

Example:
    import asyncio
    from topstepx import TopStepXAuth, TopStepXClient, OrderType, OrderSide

    async def main():
        auth = TopStepXAuth("your_username", "your_api_key")
        client = TopStepXClient(auth)
        
        # Get accounts
        accounts = await client.get_active_accounts()
        print(accounts)
        
        # Place a market order
        order = await client.place_order(
            account_id=123,
            contract_id="CON.F.US.EP.M25",
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            size=1
        )
        print(order)

    asyncio.run(main())
"""

__version__ = "0.1.0"

from .auth import TopStepXAuth
from .client import TopStepXClient
from .models import OrderType, OrderSide, OrderStatus, PositionType
from .exceptions import (
    TopStepXError,
    AuthenticationError,
    APIError,
    OrderError,
    PositionError
)

__all__ = [
    # Version
    "__version__",
    # Main classes
    "TopStepXAuth",
    "TopStepXClient",
    # Enums
    "OrderType",
    "OrderSide",
    "OrderStatus",
    "PositionType",
    # Exceptions
    "TopStepXError",
    "AuthenticationError",
    "APIError",
    "OrderError",
    "PositionError",
]
