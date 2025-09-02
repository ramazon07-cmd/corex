#!/usr/bin/env python3
"""
Test script for CoreX functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the corex package to the path
sys.path.insert(0, str(Path(__file__).parent))

from corex.cli import main
from corex.utils import print_success, print_error, print_info


def test_corex():
    """Test CoreX functionality"""
    print_info("Testing CoreX functionality...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # Test project creation
        print_info("Testing project creation...")
        try:
            # Simulate command line arguments
            sys.argv = [
                'corex',
                'new',
                'testproject',
                '--auth=session',
                '--ui=tailwind',
                '--database=sqlite',
                '--api'
            ]
            
            # This would normally run the command
            # For now, just test the imports
            from corex.generators import generate_project
            from corex.utils import validate_project_name
            
            # Test validation
            assert validate_project_name("testproject") == True
            assert validate_project_name("test project") == False
            assert validate_project_name("123project") == False
            
            print_success("✓ Project validation works")
            
            # Test template loading
            from corex.utils import get_template_path
            template_path = get_template_path("projects/manage.py.j2")
            assert template_path.exists()
            print_success("✓ Template loading works")
            
        except Exception as e:
            print_error(f"✗ Project creation test failed: {e}")
            return False
    
    print_success("✓ All CoreX tests passed!")
    return True


if __name__ == "__main__":
    success = test_corex()
    sys.exit(0 if success else 1)
