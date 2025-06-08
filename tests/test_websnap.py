import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from websnap import WebSnap, WebSnapError, NavigationError
from websnap import screenshot, screenshot_multiple

class TestWebSnap:

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def websnap(self):
        return WebSnap(headless=True, timeout=10000)

    def test_init(self):
        """Test WebSnap initialization"""
        snap = WebSnap(width=1920, height=1080, headless=False)
        assert snap.width == 1920
        assert snap.height == 1080
        assert snap.headless == False

    def test_invalid_browser_type(self):
        """Test invalid browser type raises error"""
        with pytest.raises(WebSnapError):
            WebSnap(browser_type="invalid")

    def test_normalize_url(self, websnap):
        """Test URL normalization"""
        assert websnap._normalize_url("google.com") == "https://google.com"
        assert websnap._normalize_url("http://google.com") == "http://google.com"
        assert websnap._normalize_url("https://google.com") == "https://google.com"

    def test_get_output_path(self, websnap, temp_dir):
        """Test output path generation"""
        # With explicit output
        path = websnap._get_output_path("https://google.com", "test.png")
        assert path == "test.png"
        
        # Auto-generated
        path = websnap._get_output_path("https://google.com", output_dir=temp_dir)
        assert path.startswith(temp_dir)
        assert "google.com" in path
        assert path.endswith(".png")

    @pytest.mark.asyncio
    async def test_screenshot_async(self, temp_dir):
        """Test async screenshot functionality"""
        snap = WebSnap(headless=True, timeout=15000)
        output_path = os.path.join(temp_dir, "test.png")
        
        try:
            result = await snap.screenshot_async("https://httpbin.org/html", output_path)
            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            await snap._close_browser()

    def test_screenshot_sync(self, temp_dir):
        """Test synchronous screenshot"""
        snap = WebSnap(headless=True, timeout=15000)
        output_path = os.path.join(temp_dir, "test.png")
        
        result = snap.screenshot("https://httpbin.org/html", output_path)
        assert result == output_path
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0

    def test_screenshot_multiple(self, temp_dir):
        """Test multiple screenshots"""
        snap = WebSnap(headless=True, timeout=15000)
        urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json"
        ]
        
        results = snap.screenshot_multiple(urls, temp_dir)
        assert len(results) == 2
        
        for result in results:
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0

    @pytest.mark.asyncio
    async def test_context_manager(self, temp_dir):
        """Test async context manager"""
        output_path = os.path.join(temp_dir, "context_test.png")
        
        async with WebSnap(headless=True, timeout=15000) as snap:
            result = await snap.screenshot_async("https://httpbin.org/html", output_path)
            assert os.path.exists(result)

    def test_invalid_url(self):
        """Test handling of invalid URLs"""
        snap = WebSnap(headless=True, timeout=5000)
        
        with pytest.raises(NavigationError):
            snap.screenshot("https://this-domain-definitely-does-not-exist-12345.com", "test.png")

    def test_quick_functions(self, temp_dir):
        """Test quick convenience functions"""
        # Single screenshot
        output_path = os.path.join(temp_dir, "quick.png")
        result = screenshot("https://httpbin.org/html", output_path, headless=True, timeout=15000)
        assert os.path.exists(result)
        
        # Multiple screenshots
        urls = ["https://httpbin.org/html"]
        results = screenshot_multiple(urls, temp_dir, headless=True, timeout=15000)
        assert len(results) == 1
        assert os.path.exists(results[0])