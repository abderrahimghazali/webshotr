"""
WebShotr - Website Screenshot Tool
"""

__version__ = "1.0.0"
__author__ = "AbderrahimGHAZALI"

from .webshotr import WebShotr, screenshot, screenshot_multiple
from .exceptions import WebShotrError, TimeoutError, NavigationError

__all__ = ["WebShotr", "WebShotrError", "TimeoutError", "NavigationError", "screenshot", "screenshot_multiple"]
