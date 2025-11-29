"""
AST-based Refactor Engine for Django Version Compatibility
"""

import ast
import sys
from typing import List, Dict, Any
import tempfile
import os


class DjangoRefactorEngine:
    """Engine for refactoring Django code using AST transforms"""
    
    def __init__(self):
        self.rules = self._load_refactor_rules()
        
    def _load_refactor_rules(self) -> Dict[str, Any]:
        """Load refactor rules for different Django versions"""
        return {
            "django_2_to_3": {
                "deprecated_imports": {
                    "django.utils.six": "Use Python 3 built-ins instead",
                    "django.utils.encoding.python_2_unicode_compatible": "Removed in Django 3.0",
                },
                "deprecated_functions": {
                    "django.conf.urls.url": "Use django.urls.path or django.urls.re_path",
                    "django.contrib.admin.ACTION_CHECKBOX_NAME": "Removed in Django 3.0",
                }
            },
            "django_3_to_4": {
                "deprecated_imports": {
                    "django.conf.urls.url": "Use django.urls.path or django.urls.re_path",
                    "django.utils.translation.ugettext": "Use gettext instead",
                    "django.utils.translation.ugettext_lazy": "Use gettext_lazy instead",
                    "django.utils.translation.ugettext_noop": "Use gettext_noop instead",
                    "django.utils.translation.ungettext": "Use ngettext instead",
                    "django.utils.translation.ungettext_lazy": "Use ngettext_lazy instead",
                }
            }
        }
    
    def detect_deprecated_patterns(self, source_code: str) -> List[Dict[str, Any]]:
        """Detect deprecated patterns in source code"""
        issues = []
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return [{"error": f"Syntax error in source code: {e}"}]
        
        # Check for deprecated imports
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    full_name = f"{module}.{alias.name}" if module else alias.name
                    
                    for version, rules in self.rules.items():
                        if "deprecated_imports" in rules:
                            for deprecated, replacement in rules["deprecated_imports"].items():
                                if full_name == deprecated:
                                    issues.append({
                                        "type": "deprecated_import",
                                        "pattern": deprecated,
                                        "replacement": replacement,
                                        "line": node.lineno,
                                        "version": version
                                    })
                                    
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    full_name = alias.name
                    
                    for version, rules in self.rules.items():
                        if "deprecated_imports" in rules:
                            for deprecated, replacement in rules["deprecated_imports"].items():
                                if full_name == deprecated:
                                    issues.append({
                                        "type": "deprecated_import",
                                        "pattern": deprecated,
                                        "replacement": replacement,
                                        "line": node.lineno,
                                        "version": version
                                    })
                                    
        return issues
    
    def apply_transforms(self, source_code: str, target_version: str = "django_3_to_4") -> str:
        """Apply AST transforms to update code for target Django version"""
        if target_version not in self.rules:
            raise ValueError(f"Unsupported target version: {target_version}")
            
        rules = self.rules[target_version]
        
        # For this example, we'll use a simple string replacement approach
        # In a real implementation, we would use libcst for safe AST transforms
        transformed_code = source_code
        
        if "deprecated_imports" in rules:
            for deprecated, _ in rules["deprecated_imports"].items():
                if deprecated == "django.utils.six":
                    # Special handling for six removal
                    transformed_code = self._refactor_six_usage(transformed_code)
                elif deprecated == "django.conf.urls.url":
                    transformed_code = transformed_code.replace(
                        "from django.conf.urls import url", 
                        "from django.urls import path, re_path"
                    )
                    transformed_code = transformed_code.replace(
                        "from django.conf.urls.url", 
                        "from django.urls import path, re_path"
                    )
                    
        if "deprecated_functions" in rules:
            for deprecated, replacement in rules["deprecated_functions"].items():
                if deprecated == "django.conf.urls.url":
                    # Replace url() calls with path() or re_path()
                    transformed_code = self._refactor_url_calls(transformed_code)
                    
        return transformed_code
    
    def _refactor_six_usage(self, source_code: str) -> str:
        """Refactor django.utils.six usage to Python 3 equivalents"""
        # Replace common six imports
        replacements = {
            "from django.utils.six import string_types": "",
            "from django.utils.six.moves import urllib": "import urllib",
            "from django.utils.six import StringIO": "from io import StringIO",
            "django.utils.six.string_types": "(str,)",
            "django.utils.six.text_type": "str",
            "django.utils.six.binary_type": "bytes",
            "django.utils.six.integer_types": "(int,)",
            "django.utils.six.iteritems": "dict.items",
            "django.utils.six.itervalues": "dict.values",
            "django.utils.six.iterkeys": "dict.keys",
            "django.utils.six.next": "next",
            "django.utils.six.moves.range": "range",
            "django.utils.six.moves.zip": "zip",
            "django.utils.six.moves.map": "map",
            "django.utils.six.moves.filter": "filter",
        }
        
        result = source_code
        for old, new in replacements.items():
            if new:
                result = result.replace(old, new)
            else:
                # Remove the import line
                lines = result.split('\n')
                lines = [line for line in lines if old not in line]
                result = '\n'.join(lines)
                
        return result
    
    def _refactor_url_calls(self, source_code: str) -> str:
        """Refactor url() calls to path() or re_path()"""
        # This is a simplified example - in practice, this would need
        # more sophisticated pattern matching to determine when to use
        # path vs re_path based on the regex patterns
        import re
        
        # Simple replacement for common cases
        result = re.sub(
            r'url\(\s*r?"([^"]+)"\s*,\s*([^,]+)\s*,\s*name\s*=\s*"([^"]+)"\s*\)',
            r'path("\1", \2, name="\3")',
            source_code
        )
        
        return result


def main():
    """Main entry point for AST refactoring"""
    if len(sys.argv) < 2:
        print("Usage: python ast_refactor.py <file_path> [target_version]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    target_version = sys.argv[2] if len(sys.argv) > 2 else "django_3_to_4"
    
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
            
        engine = DjangoRefactorEngine()
        
        # Detect deprecated patterns
        issues = engine.detect_deprecated_patterns(source_code)
        if issues:
            print("DEPRECATED PATTERNS DETECTED:")
            for issue in issues:
                if "error" in issue:
                    print(f"  ERROR: {issue['error']}")
                else:
                    print(f"  Line {issue['line']}: {issue['pattern']} -> {issue['replacement']} ({issue['version']})")
                    
        # Apply transforms
        transformed_code = engine.apply_transforms(source_code, target_version)
        
        # Write transformed code back to file
        with open(file_path, 'w') as f:
            f.write(transformed_code)
            
        print(f"\n✅ Successfully refactored {file_path} for {target_version}")
        
    except Exception as e:
        print(f"Error refactoring file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()