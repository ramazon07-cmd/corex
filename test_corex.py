#!/usr/bin/env python3
"""
Comprehensive test suite for CoreX
Generated for v1.0.0 release
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import subprocess
import pytest
from unittest.mock import patch, MagicMock

# Add the corex module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from corex import cli, commands, generators, utils


class TestUtils:
    """Test utility functions"""
    
    def test_validate_project_name(self):
        """Test project name validation"""
        assert utils.validate_project_name("test_project")
        assert utils.validate_project_name("testproject")
        assert utils.validate_project_name("test123")
        assert not utils.validate_project_name("test project")  # spaces
        assert not utils.validate_project_name("123test")  # starts with number
        assert not utils.validate_project_name("test-project")  # hyphens
        assert not utils.validate_project_name("")  # empty
    
    def test_get_app_templates(self):
        """Test getting available app templates"""
        templates = utils.get_app_templates()
        expected = ["blog", "portfolio", "forum", "wiki", "elearn", "social", "crm", "shop"]
        assert all(template in templates for template in expected)
    
    def test_get_auth_options(self):
        """Test getting auth options"""
        options = utils.get_auth_options()
        expected = ["jwt", "session", "allauth"]
        assert all(option in options for option in expected)
    
    def test_get_ui_options(self):
        """Test getting UI options"""
        options = utils.get_ui_options()
        expected = ["tailwind", "bootstrap", "none"]
        assert all(option in options for option in expected)
    
    def test_format_duration(self):
        """Test duration formatting"""
        assert utils.format_duration(30) == "30.0s"
        assert utils.format_duration(120) == "2.0m"
        assert utils.format_duration(3600) == "1.0h"
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        assert utils.sanitize_filename("test<file>") == "test_file_"
        assert utils.sanitize_filename("  test.file  ") == "test.file"
        assert utils.sanitize_filename("test:file") == "test_file"


class TestCLI:
    """Test CLI commands"""
    
    def test_main_command_help(self):
        """Test main command shows help"""
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--help'])
        assert result.exit_code == 0
        assert "CoreX" in result.output
        assert "Django scaffolding framework" in result.output
    
    def test_version_command(self):
        """Test version command"""
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--version'])
        assert result.exit_code == 0
        assert "1.0.0" in result.output
    
    def test_deploy_command_help(self):
        """Test deploy command shows help"""
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(cli.main, ['deploy', '--help'])
        assert result.exit_code == 0
        assert "Deploy Django project" in result.output
        assert "--platform" in result.output


if __name__ == "__main__":
    # Simple test runner when pytest is not available
    print("Running CoreX tests...")
    
    # Test utils
    test_utils = TestUtils()
    test_utils.test_validate_project_name()
    test_utils.test_get_app_templates()
    test_utils.test_get_auth_options()
    test_utils.test_get_ui_options()
    test_utils.test_format_duration()
    test_utils.test_sanitize_filename()
    print("✓ Utils tests passed")
    
    # Test CLI
    test_cli = TestCLI()
    test_cli.test_main_command_help()
    test_cli.test_version_command()
    test_cli.test_deploy_command_help()
    print("✓ CLI tests passed")
    
    print("\n🎉 All basic tests passed!")
    print("CoreX v1.0.0 is ready for release.")
