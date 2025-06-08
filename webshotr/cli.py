"""
Command Line Interface for WebShotr
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import click

from . import WebShotr, __version__
from .exceptions import WebShotrError


@click.command()
@click.argument('urls', nargs=-1, required=False)
@click.option('--output', '-o', help='Output file path (for single URL) or directory (for multiple URLs)')
@click.option('--width', '-w', default=1280, help='Viewport width', type=int)
@click.option('--height', '-h', default=720, help='Viewport height', type=int)
@click.option('--full-page', '-f', is_flag=True, help='Capture full page')
@click.option('--mobile', '-m', is_flag=True, help='Use mobile viewport')
@click.option('--quality', '-q', type=click.IntRange(1, 100), help='JPEG quality (1-100)')
@click.option('--delay', '-d', default=0, type=int, help='Delay in seconds before screenshot')
@click.option('--element', '-e', help='CSS selector for specific element')
@click.option('--browser', '-b', default='chromium', 
              type=click.Choice(['chromium', 'firefox', 'webkit']), 
              help='Browser engine to use')
@click.option('--user-agent', '-ua', help='Custom user agent string')
@click.option('--timeout', '-t', default=30, type=int, help='Page load timeout in seconds')
@click.option('--headless/--no-headless', default=True, help='Run in headless mode')
@click.option('--list-file', '-l', type=click.Path(exists=True), help='File containing list of URLs')
@click.option('--config', '-c', type=click.Path(exists=True), help='JSON config file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.version_option(__version__)
def main(
    urls: tuple,
    output: Optional[str],
    width: int,
    height: int,
    full_page: bool,
    mobile: bool,
    quality: Optional[int],
    delay: int,
    element: Optional[str],
    browser: str,
    user_agent: Optional[str],
    timeout: int,
    headless: bool,
    list_file: Optional[str],
    config: Optional[str],
    verbose: bool
):
    """
    WebShotr - Take screenshots of websites
    
    Examples:
    
    \b
    # Single URL
    webshotr https://example.com
    
    \b
    # Multiple URLs
    webshotr https://google.com https://github.com --output screenshots/
    
    \b
    # Full page screenshot
    webshotr https://example.com --full-page --output fullpage.png
    
    \b
    # Mobile viewport
    webshotr https://example.com --mobile --output mobile.png
    
    \b
    # From file
    webshotr --list-file urls.txt --output screenshots/
    
    \b
    # With config file
    webshotr https://example.com --config config.json
    """
    
    def show_banner():
        """Display the WebShotr banner"""
        banner = """
\033[92m
██╗    ██╗███████╗██████╗ ███████╗██╗  ██╗ ██████╗ ████████╗██████╗ 
██║    ██║██╔════╝██╔══██╗██╔════╝██║  ██║██╔═══██╗╚══██╔══╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝███████╗███████║██║   ██║   ██║   ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗╚════██║██╔══██║██║   ██║   ██║   ██╔══██╗
╚███╔███╔╝███████╗██████╔╝███████║██║  ██║╚██████╔╝   ██║   ██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
                                                                     
                               v1.0.0
\033[0m"""
        click.echo(banner)
    
    # If no URLs provided and no list file, show banner and help
    if not urls and not list_file:
        show_banner()
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        return
    
    # Load config file if provided
    config_data = {}
    if config:
        try:
            with open(config, 'r') as f:
                config_data = json.load(f)
                if verbose:
                    click.echo(f"Loaded config from {config}")
        except Exception as e:
            click.echo(f"Error loading config file: {e}", err=True)
            sys.exit(1)
    
    # Merge CLI args with config (CLI takes precedence)
    final_config = {**config_data}
    cli_args = {
        'width': width,
        'height': height,
        'headless': headless,
        'timeout': timeout * 1000,  # Convert to milliseconds
        'browser_type': browser,
        'user_agent': user_agent,
    }
    
    # Only override config if CLI arg was explicitly set
    for key, value in cli_args.items():
        if value is not None:
            final_config[key] = value
    
    # Collect URLs
    url_list = list(urls)
    
    # Add URLs from file if provided
    if list_file:
        try:
            with open(list_file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                url_list.extend(file_urls)
                if verbose:
                    click.echo(f"Loaded {len(file_urls)} URLs from {list_file}")
        except Exception as e:
            click.echo(f"Error reading URL list file: {e}", err=True)
            sys.exit(1)
    
    if not url_list:
        click.echo("No URLs provided", err=True)
        sys.exit(1)
    
    # Screenshot options
    screenshot_options = {
        'full_page': full_page,
        'mobile': mobile,
        'quality': quality,
        'delay': delay,
        'element': element,
    }
    
    try:
        # Initialize WebShotr
        snap = WebShotr(**final_config)
        
        if verbose:
            click.echo(f"WebShotr v{__version__}")
            click.echo(f"Browser: {browser}")
            click.echo(f"Viewport: {width}x{height}")
            click.echo(f"URLs to process: {len(url_list)}")
        
        if len(url_list) == 1:
            # Single URL
            url = url_list[0]
            if verbose:
                click.echo(f"Taking screenshot of: {url}")
            
            result = snap.screenshot(url, output, **screenshot_options)
            click.echo(f"Screenshot saved: {result}")
            
        else:
            # Multiple URLs
            output_dir = output or "screenshots"
            if verbose:
                click.echo(f"Taking screenshots of {len(url_list)} URLs")
                click.echo(f"Output directory: {output_dir}")
            
            results = snap.screenshot_multiple(url_list, output_dir, **screenshot_options)
            
            click.echo(f"Screenshots saved to {output_dir}/:")
            for i, result in enumerate(results):
                click.echo(f"  {url_list[i]} -> {os.path.basename(result)}")
    
    except WebShotrError as e:
        click.echo(f"WebShotr error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()