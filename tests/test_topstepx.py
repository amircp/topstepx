"""Tests for TopStepX client"""

import pytest
from datetime import datetime, timedelta

from topstepx import (
    TopStepXAuth,
    TopStepXClient,
    OrderType,
    OrderSide,
    OrderStatus,
    PositionType,
)


class TestModels:
    """Test model enums"""

    def test_order_type_values(self):
        assert OrderType.LIMIT == 1
        assert OrderType.MARKET == 2
        assert OrderType.STOP == 4
        assert OrderType.TRAILING_STOP == 5
        assert OrderType.JOIN_BID == 6
        assert OrderType.JOIN_ASK == 7

    def test_order_side_values(self):
        assert OrderSide.BUY == 0
        assert OrderSide.SELL == 1

    def test_order_status_values(self):
        assert OrderStatus.PENDING == 1
        assert OrderStatus.FILLED == 2
        assert OrderStatus.CANCELLED == 3
        assert OrderStatus.REJECTED == 4

    def test_position_type_values(self):
        assert PositionType.LONG == 0
        assert PositionType.SHORT == 1


class TestAuth:
    """Test authentication class"""

    def test_auth_initialization(self):
        auth = TopStepXAuth("test_user", "test_key")
        assert auth.username == "test_user"
        assert auth.api_key == "test_key"
        assert auth.token is None
        assert auth.token_expires is None

    def test_token_expired_no_token(self):
        auth = TopStepXAuth("test_user", "test_key")
        assert auth._is_token_expired() is True

    def test_token_expired_with_future_expiry(self):
        auth = TopStepXAuth("test_user", "test_key")
        auth.token = "test_token"
        auth.token_expires = datetime.now() + timedelta(hours=1)
        assert auth._is_token_expired() is False

    def test_token_expired_with_past_expiry(self):
        auth = TopStepXAuth("test_user", "test_key")
        auth.token = "test_token"
        auth.token_expires = datetime.now() - timedelta(hours=1)
        assert auth._is_token_expired() is True

    def test_token_expired_within_margin(self):
        auth = TopStepXAuth("test_user", "test_key")
        auth.token = "test_token"
        # Expires in 3 minutes, but margin is 5 minutes
        auth.token_expires = datetime.now() + timedelta(minutes=3)
        assert auth._is_token_expired() is True

    def test_get_headers(self):
        auth = TopStepXAuth("test_user", "test_key")
        auth.token = "my_token"
        headers = auth.get_headers()
        assert headers == {"Authorization": "Bearer my_token"}


class TestClient:
    """Test client class"""

    def test_client_initialization(self):
        auth = TopStepXAuth("test_user", "test_key")
        client = TopStepXClient(auth)
        assert client.auth is auth
        assert client.BASE_URL == "https://api.topstepx.com"


# Integration tests would require mocking httpx or a test server
# Example structure for async integration tests:
#
# @pytest.mark.asyncio
# async def test_get_active_accounts(mocker):
#     # Mock the httpx client
#     mock_response = mocker.Mock()
#     mock_response.json.return_value = {
#         "success": True,
#         "errorCode": 0,
#         "accounts": [{"id": 1, "name": "Test"}]
#     }
#     ...
