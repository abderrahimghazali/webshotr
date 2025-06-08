"""
WebSnap - Website Screenshot Tool
"""

__version__ = "1.0.0"
__author__ = "YourName"

from .websnap import WebSnap, screenshot, screenshot_multiple
from .exceptions import WebSnapError, TimeoutError, NavigationError

__all__ = ["WebSnap", "WebSnapError", "TimeoutError", "NavigationError", "screenshot", "screenshot_multiple"]