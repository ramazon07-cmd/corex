"""
CoreX App Generator
Generates Django apps from templates
"""

import os
from pathlib import Path
from typing import Dict, Optional

from .base_generator import BaseGenerator
from ..utils import (
    create_directory,
    get_template_path,
    print_error,
    print_info,
    print_success,
    print_warning,
)


class AppGenerator(BaseGenerator):
    """Generator for Django apps"""
    
    def __init__(self):
        super().__init__("apps")
    
    def generate(self, output_path: Path, context: Dict) -> bool:
        """Generate a Django app with CoreX"""
        try:
            # Create app directory
            create_directory(output_path)
            
            # Generate app structure
            self._generate_app_structure(output_path, context)
            
            # Generate app-specific files based on type
            if context.get("app_type"):
                self._generate_app_type_files(output_path, context["app_type"], context)
            
            # Generate seed data if requested
            if context.get("seed", False):
                self._generate_seed_data(output_path, context.get("app_type"), context)
            
            print_success(f"App '{context['app_name']}' generated successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to generate app: {e}")
            return False
    
    def _generate_app_structure(self, app_path: Path, context: Dict) -> None:
        """Generate basic app structure"""
        app_name = context["app_name"]
        
        # Create __init__.py
        (app_path / "__init__.py").touch()
        
        # Create apps.py
        apps_content = self._render_template("apps.py.j2", context)
        self._write_file(app_path / "apps.py", apps_content)
        
        # Create models.py
        models_content = self._render_template("models.py.j2", context)
        self._write_file(app_path / "models.py", models_content)
        
        # Create views.py
        views_content = self._render_template("views.py.j2", context)
        self._write_file(app_path / "views.py", views_content)
        
        # Create urls.py
        urls_content = self._render_template("urls.py.j2", context)
        self._write_file(app_path / "urls.py", urls_content)
        
        # Create admin.py
        admin_content = self._render_template("admin.py.j2", context)
        self._write_file(app_path / "admin.py", admin_content)
        
        # Create tests directory
        tests_dir = app_path / "tests"
        create_directory(tests_dir)
        (tests_dir / "__init__.py").touch()
        
        # Create test files
        test_files = [
            "test_models.py",
            "test_views.py",
        ]
        
        for filename in test_files:
            content = self._render_template(f"tests/{filename}.j2", context)
            self._write_file(tests_dir / filename, content)
        
        # Create migrations directory
        migrations_dir = app_path / "migrations"
        create_directory(migrations_dir)
        (migrations_dir / "__init__.py").touch()
        
        # Create templates directory if UI is enabled
        if context.get("ui", "none") != "none":
            templates_dir = app_path / "templates" / app_name
            create_directory(templates_dir)
            
            # Generate templates
            template_files = [
                "list.html",
                "detail.html",
                "form.html",
            ]
            
            for filename in template_files:
                content = self._render_template(f"templates/{filename}.j2", context)
                self._write_file(templates_dir / filename, content)
        
        # Create API files if API is enabled
        if context.get("api", False):
            api_dir = app_path / "api"
            create_directory(api_dir)
            (api_dir / "__init__.py").touch()
            
            api_files = [
                "serializers.py",
                "views.py",
                "urls.py",
            ]
            
            for filename in api_files:
                content = self._render_template(f"api/{filename}.j2", context)
                self._write_file(api_dir / filename, content)
    
    def _generate_app_type_files(self, app_path: Path, app_type: str, context: Dict) -> None:
        """Generate app-specific files based on type"""
        try:
            # Get app-specific template
            template = self.env.get_template(f"types/{app_type}.py.j2")
            content = template.render(**context)
            
            # Replace the main models.py file with app-specific models
            models_file = app_path / "models.py"
            
            # Replace the entire content with app-specific models
            models_file.write_text(content)
            
            print_info(f"Generated {app_type}-specific models")
            
        except Exception as e:
            print_warning(f"Could not generate {app_type}-specific files: {e}")
    
    def _generate_seed_data(self, app_path: Path, app_type: Optional[str], context: Dict) -> None:
        """Generate seed data for the app"""
        try:
            # Create management commands directory
            management_dir = app_path / "management"
            create_directory(management_dir)
            (management_dir / "__init__.py").touch()
            
            commands_dir = management_dir / "commands"
            create_directory(commands_dir)
            (commands_dir / "__init__.py").touch()
            
            # Generate seed command
            seed_content = self._render_template("management/seed.py.j2", context)
            self._write_file(commands_dir / "seed.py", seed_content)
            
            print_info("Generated seed data command")
            
        except Exception as e:
            print_warning(f"Could not generate seed data: {e}")