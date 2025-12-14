"""TopStepX API Exceptions"""


class TopStepXError(Exception):
    """Base exception for TopStepX API errors"""
    def __init__(self, message: str, error_code: int = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(TopStepXError):
    """Raised when authentication fails"""
    pass


class APIError(TopStepXError):
    """Raised when an API call fails"""
    pass


class OrderError(TopStepXError):
    """Raised when an order operation fails"""
    pass


class PositionError(TopStepXError):
    """Raised when a position operation fails"""
    pass
