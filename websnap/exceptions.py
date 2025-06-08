"""
Custom exceptions for WebSnap
"""

class WebSnapError(Exception):
    """Base exception for WebSnap"""
    pass

class TimeoutError(WebSnapError):
    """Raised when operation times out"""
    pass

class NavigationError(WebSnapError):
    """Raised when navigation fails"""
    pass