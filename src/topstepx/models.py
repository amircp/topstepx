"""TopStepX API Models and Enums"""

from enum import IntEnum


class OrderType(IntEnum):
    """Tipo de orden"""
    LIMIT = 1
    MARKET = 2
    STOP = 4
    TRAILING_STOP = 5
    JOIN_BID = 6
    JOIN_ASK = 7


class OrderSide(IntEnum):
    """Lado de la orden"""
    BUY = 0   # Bid
    SELL = 1  # Ask


class OrderStatus(IntEnum):
    """Estado de la orden"""
    PENDING = 1    # Orden abierta/pendiente
    FILLED = 2     # Orden ejecutada
    CANCELLED = 3  # Orden cancelada
    REJECTED = 4   # Orden rechazada


class PositionType(IntEnum):
    """Tipo de posición"""
    LONG = 0
    SHORT = 1
