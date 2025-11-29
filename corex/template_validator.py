"""
Template Compiler/Validator for CoreX Industry Templates
"""

import os
import sys
import yaml
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from jinja2 import Environment, FileSystemLoader


class TemplateValidator:
    """Validates and compiles CoreX industry templates"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict:
        """Load template metadata from YAML file"""
        metadata_file = self.template_path / "metadata.yml"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
            
        with open(metadata_file, 'r') as f:
            return yaml.safe_load(f)
    
    def validate_structure(self) -> List[str]:
        """Validate template directory structure"""
        issues = []
        
        # Check required files
        required_files = [
            "metadata.yml",
            "schema.json",
            "generators.py",
        ]
        
        for file in required_files:
            if not (self.template_path / file).exists():
                issues.append(f"Missing required file: {file}")
        
        # Check tests directory
        if not (self.template_path / "tests").exists():
            issues.append("Missing tests directory")
            
        return issues
    
    def validate_models(self) -> List[str]:
        """Validate required domain models"""
        issues = []
        
        # Check if models.py exists
        models_file = self.template_path / "models.py"
        if not models_file.exists():
            issues.append("Missing models.py file")
            return issues
            
        # Check for migrations
        migrations_dir = self.template_path / "migrations"
        if not migrations_dir.exists():
            issues.append("Missing migrations directory")
        elif not any(migrations_dir.iterdir()):
            issues.append("Migrations directory is empty")
            
        return issues
    
    def run_static_analysis(self) -> Tuple[bool, List[str]]:
        """Run static analysis with pyright/mypy"""
        issues = []
        
        try:
            # Try pyright first
            result = subprocess.run(
                ["pyright", str(self.template_path)], 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                issues.extend(result.stdout.split('\n'))
                issues.extend(result.stderr.split('\n'))
                
        except FileNotFoundError:
            try:
                # Fallback to mypy
                result = subprocess.run(
                    ["mypy", str(self.template_path)], 
                    capture_output=True, 
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    issues.extend(result.stdout.split('\n'))
                    issues.extend(result.stderr.split('\n'))
                    
            except FileNotFoundError:
                issues.append("Neither pyright nor mypy found for static analysis")
                
        except subprocess.TimeoutExpired:
            issues.append("Static analysis timed out")
        except Exception as e:
            issues.append(f"Static analysis failed: {str(e)}")
            
        return len(issues) == 0, issues
    
    def generate_compatibility_report(self) -> Dict:
        """Generate template compatibility report"""
        report = {
            "template_name": self.template_path.name,
            "version": self.metadata.get("version", "1.0.0"),
            "validation": {
                "structure": self.validate_structure(),
                "models": self.validate_models(),
            },
            "analysis": {},
            "compatibility": {}
        }
        
        # Run static analysis
        analysis_success, analysis_issues = self.run_static_analysis()
        report["analysis"] = {
            "success": analysis_success,
            "issues": analysis_issues
        }
        
        return report


def main():
    """Main entry point for template validation"""
    if len(sys.argv) < 2:
        print("Usage: python template_validator.py <template_path>")
        sys.exit(1)
        
    template_path = sys.argv[1]
    
    try:
        validator = TemplateValidator(template_path)
        report = validator.generate_compatibility_report()
        
        print(json.dumps(report, indent=2))
        
        # Check for critical issues
        critical_issues = 0
        for category, issues in report["validation"].items():
            if issues:
                print(f"\n{category.upper()} ISSUES:")
                for issue in issues:
                    print(f"  - {issue}")
                critical_issues += len(issues)
                
        if not report["analysis"]["success"]:
            print("\nSTATIC ANALYSIS ISSUES:")
            for issue in report["analysis"]["issues"]:
                if issue.strip():
                    print(f"  - {issue}")
                    
        if critical_issues == 0 and report["analysis"]["success"]:
            print("\n✅ Template validation passed!")
            sys.exit(0)
        else:
            print(f"\n❌ Template validation failed with {critical_issues} critical issues")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error validating template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()