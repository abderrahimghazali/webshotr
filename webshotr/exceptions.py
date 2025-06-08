"""
Custom exceptions for WebShotr
"""

class WebShotrError(Exception):
    """Base exception for WebShotr"""
    pass

class TimeoutError(WebShotrError):
    """Raised when operation times out"""
    pass

class NavigationError(WebShotrError):
    """Raised when navigation fails"""
    pass