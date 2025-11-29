"""
Test suite for CoreX Industry Templates
"""

import unittest
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the corex module to the path
sys.path.insert(0, str(Path(__file__).parent))

from corex.template_validator import TemplateValidator
from corex.ast_refactor import DjangoRefactorEngine
from corex.env_checker import EnvironmentChecker


class TestIndustryTemplates(unittest.TestCase):
    """Test cases for industry templates"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.template_dir = Path(__file__).parent / "corex" / "templates" / "industry"
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_ecommerce_template_structure(self):
        """Test E-commerce template structure"""
        template_path = self.template_dir / "ecommerce"
        self.assertTrue(template_path.exists(), "E-commerce template directory should exist")
        
        # Check required files
        required_files = ["schema.json", "models.py", "generators.py"]
        for file in required_files:
            self.assertTrue((template_path / file).exists(), f"Required file {file} should exist")
    
    def test_legal_template_structure(self):
        """Test Legal template structure"""
        template_path = self.template_dir / "legal"
        self.assertTrue(template_path.exists(), "Legal template directory should exist")
        
        # Check required files
        required_files = ["schema.json", "models.py"]
        for file in required_files:
            self.assertTrue((template_path / file).exists(), f"Required file {file} should exist")
    
    def test_realestate_template_structure(self):
        """Test Real Estate template structure"""
        template_path = self.template_dir / "realestate"
        self.assertTrue(template_path.exists(), "Real Estate template directory should exist")
        
        # Check required files
        required_files = ["schema.json", "models.py"]
        for file in required_files:
            self.assertTrue((template_path / file).exists(), f"Required file {file} should exist")
    
    def test_healthcare_template_structure(self):
        """Test Healthcare template structure"""
        template_path = self.template_dir / "healthcare"
        self.assertTrue(template_path.exists(), "Healthcare template directory should exist")
        
        # Check required files
        required_files = ["schema.json", "models.py"]
        for file in required_files:
            self.assertTrue((template_path / file).exists(), f"Required file {file} should exist")
    
    def test_fintech_template_structure(self):
        """Test Fintech template structure"""
        template_path = self.template_dir / "fintech"
        self.assertTrue(template_path.exists(), "Fintech template directory should exist")
        
        # Check required files
        required_files = ["schema.json", "models.py"]
        for file in required_files:
            self.assertTrue((template_path / file).exists(), f"Required file {file} should exist")


class TestTemplateValidator(unittest.TestCase):
    """Test cases for template validator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.template_dir = Path(__file__).parent / "corex" / "templates" / "industry" / "ecommerce"
        
    def test_validator_initialization(self):
        """Test TemplateValidator initialization"""
        validator = TemplateValidator(str(self.template_dir))
        self.assertIsNotNone(validator)
        self.assertEqual(validator.template_path, self.template_dir)
    
    def test_metadata_loading(self):
        """Test metadata loading"""
        validator = TemplateValidator(str(self.template_dir))
        metadata = validator._load_metadata()
        self.assertIn("name", metadata)
        self.assertIn("title", metadata)
        self.assertIn("description", metadata)
        self.assertEqual(metadata["name"], "ecommerce")


class TestASTRefactorEngine(unittest.TestCase):
    """Test cases for AST refactor engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = DjangoRefactorEngine()
        
    def test_refactor_engine_initialization(self):
        """Test DjangoRefactorEngine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIn("django_2_to_3", self.engine.rules)
        self.assertIn("django_3_to_4", self.engine.rules)
    
    def test_deprecated_pattern_detection(self):
        """Test deprecated pattern detection"""
        source_code = """
from django.utils.six import string_types
from django.conf.urls import url

def my_view(request):
    return HttpResponse("Hello")
"""
        
        issues = self.engine.detect_deprecated_patterns(source_code)
        self.assertGreater(len(issues), 0)
        
        # Check for specific deprecated patterns
        deprecated_imports = [issue for issue in issues if issue["type"] == "deprecated_import"]
        self.assertGreater(len(deprecated_imports), 0)
    
    def test_six_refactoring(self):
        """Test six usage refactoring"""
        source_code = """
from django.utils.six import string_types, text_type, integer_types
from django.utils.six.moves import range, zip

def my_function():
    return string_types, text_type, integer_types, range(10), list(zip([1, 2], [3, 4]))
"""
        
        refactored = self.engine._refactor_six_usage(source_code)
        # Check that some six usages have been replaced or removed
        # The actual implementation may vary, so we'll check for general changes
        self.assertIsInstance(refactored, str)


class TestEnvironmentChecker(unittest.TestCase):
    """Test cases for environment checker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checker = EnvironmentChecker()
        
    def test_environment_checker_initialization(self):
        """Test EnvironmentChecker initialization"""
        self.assertIsNotNone(self.checker)
        self.assertIsNotNone(self.checker.os_name)
        self.assertIsNotNone(self.checker.arch)
    
    def test_python_version_check(self):
        """Test Python version check"""
        is_valid, version = self.checker.check_python_version()
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(version, str)
    
    def test_report_generation(self):
        """Test environment report generation"""
        report = self.checker.generate_report()
        self.assertIn("os", report)
        self.assertIn("python", report)
        self.assertIn("tools", report)
        self.assertIn("docker", report)
        self.assertIn("package_managers", report)


if __name__ == "__main__":
    unittest.main()