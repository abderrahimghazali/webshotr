"""
Main WebSnap class for taking website screenshots
"""

import asyncio
import os
import time
from pathlib import Path
from typing import Optional, Union, Dict, Any, List
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Browser, Page
from PIL import Image

from .exceptions import WebSnapError, TimeoutError, NavigationError


class WebSnap:
    """
    WebSnap - Easy website screenshot tool
    
    Examples:
        Basic usage:
        >>> snap = WebSnap()
        >>> snap.screenshot("https://example.com", "screenshot.png")
        
        With options:
        >>> snap = WebSnap(width=1920, height=1080, headless=True)
        >>> snap.screenshot("https://github.com", "github.png", full_page=True)
        
        Multiple URLs:
        >>> urls = ["https://google.com", "https://github.com"]
        >>> snap.screenshot_multiple(urls, output_dir="screenshots")
    """
    
    def __init__(
        self,
        width: int = 1280,
        height: int = 720,
        headless: bool = True,
        timeout: int = 30000,
        browser_type: str = "chromium",
        user_agent: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize WebSnap
        
        Args:
            width: Viewport width in pixels
            height: Viewport height in pixels  
            headless: Run browser in headless mode
            timeout: Page load timeout in milliseconds
            browser_type: Browser to use ('chromium', 'firefox', 'webkit')
            user_agent: Custom user agent string
        """
        self.width = width
        self.height = height
        self.headless = headless
        self.timeout = timeout
        self.browser_type = browser_type.lower()
        self.user_agent = user_agent
        self.browser: Optional[Browser] = None
        self.playwright = None
        
        # Validate browser type
        if self.browser_type not in ["chromium", "firefox", "webkit"]:
            raise WebSnapError(f"Unsupported browser type: {browser_type}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._start_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self._close_browser()
    
    async def _start_browser(self):
        """Start the browser"""
        if self.playwright is None:
            self.playwright = await async_playwright().start()
            
        if self.browser_type == "chromium":
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
        elif self.browser_type == "firefox":
            self.browser = await self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = await self.playwright.webkit.launch(headless=self.headless)
    
    async def _close_browser(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    
    def _normalize_url(self, url: str) -> str:
        """Add protocol if missing"""
        if not url.startswith(('http://', 'https://')):
            return f'https://{url}'
        return url
    
    def _get_output_path(self, url: str, output: Optional[str] = None, output_dir: str = ".") -> str:
        """Generate output path if not provided"""
        if output:
            return output
            
        # Generate filename from URL
        parsed = urlparse(self._normalize_url(url))
        domain = parsed.netloc.replace("www.", "")
        path = parsed.path.replace("/", "_").strip("_") or "index"
        timestamp = int(time.time() * 1000)  # Use milliseconds for better uniqueness
        filename = f"{domain}_{path}_{timestamp}.png"
        
        return os.path.join(output_dir, filename)
    
    async def _take_screenshot(
        self,
        url: str,
        output_path: str,
        full_page: bool = False,
        mobile: bool = False,
        quality: Optional[int] = None,
        delay: int = 0,
        element_selector: Optional[str] = None,
        **kwargs
    ) -> str:
        """Internal screenshot method"""
        
        # Ensure browser is running
        if not self.browser:
            await self._start_browser()
        
        # Create new page
        page = await self.browser.new_page()
        
        try:
            # Set viewport
            if mobile:
                # iPhone 12 Pro dimensions
                await page.set_viewport_size({"width": 390, "height": 844})
                if not self.user_agent:
                    await page.set_extra_http_headers({
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15"
                    })
            else:
                await page.set_viewport_size({"width": self.width, "height": self.height})
            
            # Set custom user agent if provided
            if self.user_agent:
                await page.set_extra_http_headers({"User-Agent": self.user_agent})
            
            # Navigate to URL
            normalized_url = self._normalize_url(url)
            try:
                await page.goto(normalized_url, timeout=self.timeout)
            except Exception as e:
                raise NavigationError(f"Failed to navigate to {normalized_url}: {str(e)}")
            
            # Wait for additional delay if specified
            if delay > 0:
                await page.wait_for_timeout(delay * 1000)
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
            
            # Take screenshot
            screenshot_options = {
                "path": output_path,
                "full_page": full_page,
            }
            
            # Add quality for JPEG
            if output_path.lower().endswith(('.jpg', '.jpeg')) and quality:
                screenshot_options["quality"] = quality
            
            if element_selector:
                # Screenshot specific element
                element = await page.query_selector(element_selector)
                if element:
                    await element.screenshot(**screenshot_options)
                else:
                    raise WebSnapError(f"Element not found: {element_selector}")
            else:
                # Screenshot entire page/viewport
                await page.screenshot(**screenshot_options)
            
            return output_path
            
        finally:
            await page.close()
    
    async def screenshot_async(
        self,
        url: str,
        output: Optional[str] = None,
        full_page: bool = False,
        mobile: bool = False,
        quality: Optional[int] = None,
        delay: int = 0,
        element: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Take a screenshot asynchronously
        
        Args:
            url: Website URL to screenshot
            output: Output file path (auto-generated if None)
            full_page: Capture full page instead of viewport
            mobile: Use mobile viewport
            quality: JPEG quality (1-100, only for .jpg/.jpeg)
            delay: Wait time in seconds before screenshot
            element: CSS selector for specific element
            
        Returns:
            Path to saved screenshot
        """
        output_path = self._get_output_path(url, output)
        return await self._take_screenshot(
            url, output_path, full_page, mobile, quality, delay, element, **kwargs
        )
    
    def screenshot(
        self,
        url: str,
        output: Optional[str] = None,
        full_page: bool = False,
        mobile: bool = False,
        quality: Optional[int] = None,
        delay: int = 0,
        element: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Take a screenshot (synchronous wrapper)
        
        Args:
            url: Website URL to screenshot
            output: Output file path (auto-generated if None)
            full_page: Capture full page instead of viewport
            mobile: Use mobile viewport
            quality: JPEG quality (1-100, only for .jpg/.jpeg)
            delay: Wait time in seconds before screenshot
            element: CSS selector for specific element
            
        Returns:
            Path to saved screenshot
        """
        return asyncio.run(
            self.screenshot_async(url, output, full_page, mobile, quality, delay, element, **kwargs)
        )
    
    async def screenshot_multiple_async(
        self,
        urls: List[str],
        output_dir: str = "screenshots",
        **kwargs
    ) -> List[str]:
        """
        Take screenshots of multiple URLs asynchronously
        
        Args:
            urls: List of URLs to screenshot
            output_dir: Directory to save screenshots
            **kwargs: Additional arguments passed to screenshot_async
            
        Returns:
            List of paths to saved screenshots
        """
        os.makedirs(output_dir, exist_ok=True)
        
        tasks = []
        for url in urls:
            output_path = self._get_output_path(url, output_dir=output_dir)
            tasks.append(self._take_screenshot(url, output_path, **kwargs))
        
        return await asyncio.gather(*tasks, return_exceptions=False)
    
    def screenshot_multiple(
        self,
        urls: List[str],
        output_dir: str = "screenshots",
        **kwargs
    ) -> List[str]:
        """
        Take screenshots of multiple URLs (synchronous wrapper)
        
        Args:
            urls: List of URLs to screenshot
            output_dir: Directory to save screenshots
            **kwargs: Additional arguments passed to screenshot
            
        Returns:
            List of paths to saved screenshots
        """
        return asyncio.run(self.screenshot_multiple_async(urls, output_dir, **kwargs))


# Quick usage functions for convenience
def screenshot(url: str, output: Optional[str] = None, **kwargs) -> str:
    """
    Quick screenshot function
    
    Args:
        url: Website URL
        output: Output file path
        **kwargs: Additional options
        
    Returns:
        Path to saved screenshot
    """
    snap = WebSnap(**kwargs)
    return snap.screenshot(url, output, **kwargs)


def screenshot_multiple(urls: List[str], output_dir: str = "screenshots", **kwargs) -> List[str]:
    """
    Quick multiple screenshot function
    
    Args:
        urls: List of URLs
        output_dir: Output directory
        **kwargs: Additional options
        
    Returns:
        List of paths to saved screenshots
    """
    snap = WebSnap(**kwargs)
    return snap.screenshot_multiple(urls, output_dir, **kwargs)