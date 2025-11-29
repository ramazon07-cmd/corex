"""
CoreX Base Generator
Abstract base class for all generators
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader

from ..utils import (
    create_directory,
    get_template_path,
    print_error,
    print_info,
    print_success,
    print_warning,
)


class BaseGenerator(ABC):
    """Abstract base class for all generators"""
    
    def __init__(self, template_type: str):
        self.template_type = template_type
        self.templates_dir = get_template_path(template_type)
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    @abstractmethod
    def generate(self, output_path: Path, context: Dict) -> bool:
        """Generate files based on templates and context"""
        pass
    
    def _render_template(self, template_name: str, context: Dict) -> str:
        """Render a template with the given context"""
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            print_error(f"Failed to render template {template_name}: {e}")
            return ""
    
    def _write_file(self, file_path: Path, content: str) -> bool:
        """Write content to a file"""
        try:
            # Create parent directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content to file
            file_path.write_text(content)
            return True
        except Exception as e:
            print_error(f"Failed to write file {file_path}: {e}")
            return False
    
    def _copy_file(self, source_path: Path, dest_path: Path) -> bool:
        """Copy a file from source to destination"""
        try:
            # Create parent directories if they don't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            import shutil
            shutil.copy2(source_path, dest_path)
            return True
        except Exception as e:
            print_error(f"Failed to copy file from {source_path} to {dest_path}: {e}")
            return False