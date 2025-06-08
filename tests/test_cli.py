import pytest
import tempfile
import os
from click.testing import CliRunner
from webshotr.cli import main

class TestCLI:
    
    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_version(self, runner):
        """Test version command"""
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output

    def test_help(self, runner):
        """Test help command"""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'WebShotr' in result.output

    def test_single_url(self, runner, temp_dir):
        """Test single URL screenshot"""
        output_file = os.path.join(temp_dir, "cli_test.png")
        result = runner.invoke(main, [
            'https://httpbin.org/html',
            '--output', output_file,
            '--timeout', '15'
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(output_file)

    def test_multiple_urls(self, runner, temp_dir):
        """Test multiple URLs"""
        result = runner.invoke(main, [
            'https://httpbin.org/html',
            'https://httpbin.org/json',
            '--output', temp_dir,
            '--timeout', '15'
        ])
        
        assert result.exit_code == 0
        # Check that files were created
        files = os.listdir(temp_dir)
        assert len(files) >= 2

    def test_url_list_file(self, runner, temp_dir):
        """Test URL list file option"""
        # Create URL list file
        url_file = os.path.join(temp_dir, "urls.txt")
        with open(url_file, 'w') as f:
            f.write("https://httpbin.org/html\n")
            f.write("# This is a comment\n")
            f.write("https://httpbin.org/json\n")
        
        result = runner.invoke(main, [
            '--list-file', url_file,
            '--output', temp_dir,
            '--timeout', '15'
        ])
        
        assert result.exit_code == 0
        files = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
        assert len(files) >= 2

    def test_mobile_option(self, runner, temp_dir):
        """Test mobile viewport option"""
        output_file = os.path.join(temp_dir, "mobile_test.png")
        result = runner.invoke(main, [
            'https://httpbin.org/html',
            '--mobile',
            '--output', output_file,
            '--timeout', '15'
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(output_file)

    def test_full_page_option(self, runner, temp_dir):
        """Test full page option"""
        output_file = os.path.join(temp_dir, "fullpage_test.png")
        result = runner.invoke(main, [
            'https://httpbin.org/html',
            '--full-page',
            '--output', output_file,
            '--timeout', '15'
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(output_file)

    def test_no_urls(self, runner):
        """Test banner and help when no URLs provided"""
        result = runner.invoke(main, [])
        assert result.exit_code == 0
        assert "██╗" in result.output  # Check for the ASCII banner 
        assert "Usage:" in result.output