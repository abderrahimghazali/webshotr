# WebShotr 📸

A simple, fast, and elegant website screenshot tool built with Python and Playwright.

![WebShotr Logo](https://i.imgur.com/FsL8MlY.png)

## ✨ Features

- 🚀 **Fast and Reliable** - Built on Playwright for robust browser automation
- 🌐 **Multi-Browser Support** - Chromium, Firefox, and WebKit
- 📱 **Mobile Screenshots** - Capture mobile viewport screenshots
- 📄 **Full Page Capture** - Take full-page screenshots beyond the viewport
- 🎯 **Element Selection** - Screenshot specific elements using CSS selectors
- 📁 **Batch Processing** - Process multiple URLs from command line or file
- ⚙️ **Configurable** - Extensive customization options
- 💻 **CLI & API** - Use from command line or integrate into Python projects
- 🎨 **Beautiful CLI** - Elegant command-line interface with colored output

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- pip

### Install WebShotr

```bash
pip install webshotr
```

### Install Playwright Browsers

After installing WebShotr, you need to install the browser binaries:

```bash
playwright install
```

## 🚀 Quick Start

### Command Line Usage

Take a screenshot of a website:

```bash
webshotr https://example.com
```

See the beautiful banner and help:

```bash
webshotr
```

### Python API Usage

```python
from webshotr import WebShotr

# Create WebShotr instance
snap = WebShotr()

# Take a screenshot
snap.screenshot("https://example.com", "screenshot.png")
```

## 📖 Usage Examples

### CLI Examples

#### Single Website

```bash
# Basic screenshot
webshotr https://example.com

# Custom output path
webshotr https://example.com --output my-screenshot.png

# Full page screenshot
webshotr https://example.com --full-page --output fullpage.png
```

#### Mobile Screenshots

```bash
# Mobile viewport
webshotr https://example.com --mobile --output mobile.png

# Custom mobile dimensions
webshotr https://example.com --width 375 --height 812 --output iphone.png
```

#### Multiple Websites

```bash
# Multiple URLs
webshotr https://google.com https://github.com --output screenshots/

# From file
webshotr --list-file urls.txt --output screenshots/
```

#### Advanced Options

```bash
# Custom browser, quality, and delay
webshotr https://example.com \
  --browser firefox \
  --quality 90 \
  --delay 3 \
  --timeout 30

# Screenshot specific element
webshotr https://example.com \
  --element "#main-content" \
  --output element.png

# Use configuration file
webshotr https://example.com --config config.json
```

### Python API Examples

#### Basic Usage

```python
from webshotr import WebShotr, screenshot

# Quick function
screenshot("https://example.com", "output.png")

# With options
screenshot("https://example.com", "output.png", 
          full_page=True, mobile=True)
```

#### Advanced Usage

```python
from webshotr import WebShotr

# Create instance with custom settings
snap = WebShotr(
    width=1920,
    height=1080,
    browser_type="firefox",
    headless=True
)

# Take screenshots
snap.screenshot("https://example.com", "desktop.png")
snap.screenshot("https://example.com", "mobile.png", mobile=True)

# Multiple URLs
urls = ["https://google.com", "https://github.com"]
results = snap.screenshot_multiple(urls, "screenshots/")
print(f"Saved {len(results)} screenshots")
```

#### Async Usage

```python
import asyncio
from webshotr import WebShotr

async def take_screenshots():
    async with WebShotr() as snap:
        # Async screenshot
        result = await snap.screenshot_async(
            "https://example.com", 
            "async-screenshot.png"
        )
        print(f"Screenshot saved: {result}")

# Run async function
asyncio.run(take_screenshots())
```

## ⚙️ Configuration

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output, -o` | Output file path or directory | Auto-generated |
| `--width, -w` | Viewport width | 1280 |
| `--height, -h` | Viewport height | 720 |
| `--full-page, -f` | Capture full page | False |
| `--mobile, -m` | Use mobile viewport | False |
| `--quality, -q` | JPEG quality (1-100) | Auto |
| `--delay, -d` | Delay before screenshot (seconds) | 0 |
| `--element, -e` | CSS selector for specific element | None |
| `--browser, -b` | Browser engine (chromium/firefox/webkit) | chromium |
| `--user-agent, -ua` | Custom user agent string | Auto |
| `--timeout, -t` | Page load timeout (seconds) | 30 |
| `--headless/--no-headless` | Run in headless mode | True |
| `--list-file, -l` | File containing list of URLs | None |
| `--config, -c` | JSON configuration file | None |
| `--verbose, -v` | Verbose output | False |

### Configuration File

Create a `config.json` file:

```json
{
  "width": 1920,
  "height": 1080,
  "headless": true,
  "timeout": 30000,
  "browser_type": "chromium",
  "user_agent": "Mozilla/5.0 (compatible; WebShotr/1.0)"
}
```

Use it with:

```bash
webshotr https://example.com --config config.json
```

### URL List File

Create a `urls.txt` file:

```
https://example.com
https://google.com
# This is a comment
https://github.com
```

Use it with:

```bash
webshotr --list-file urls.txt --output screenshots/
```

## 🐍 API Reference

### WebShotr Class

```python
WebShotr(
    width: int = 1280,
    height: int = 720,
    headless: bool = True,
    timeout: int = 30000,
    browser_type: str = "chromium",
    user_agent: Optional[str] = None
)
```

#### Methods

- `screenshot(url, output=None, **kwargs)` - Take a screenshot
- `screenshot_multiple(urls, output_dir="screenshots", **kwargs)` - Multiple screenshots
- `screenshot_async(url, output=None, **kwargs)` - Async screenshot
- `screenshot_multiple_async(urls, output_dir="screenshots", **kwargs)` - Async multiple

### Convenience Functions

```python
from webshotr import screenshot, screenshot_multiple

# Quick screenshot
screenshot("https://example.com", "output.png")

# Multiple screenshots
screenshot_multiple(urls, "screenshots/")
```

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/abderrahimghazali/webshotr.git
cd webshotr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-asyncio flake8

# Install Playwright browsers
playwright install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_cli.py -v

# Run with coverage
pytest tests/ --cov=webshotr
```

### Code Style

```bash
# Check code style
flake8 webshotr/ tests/

# Format code (if you have black installed)
black webshotr/ tests/
```

## 📝 Requirements

- Python 3.7+
- playwright >= 1.40.0
- Pillow >= 9.0.0
- click >= 8.0.0
- aiofiles >= 22.0.0

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [Playwright](https://playwright.dev/) for reliable browser automation
- Inspired by the need for a simple, elegant screenshot tool
- Thanks to all contributors and users

## 📬 Support

- 🐛 [Report Issues](https://github.com/abderrahimghazali/webshotr/issues)
- 💡 [Feature Requests](https://github.com/abderrahimghazali/webshotr/issues)

---

Made with ❤️ by [AbderrahimGHAZALI](https://github.com/abderrahimghazali) 