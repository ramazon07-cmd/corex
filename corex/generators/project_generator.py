"""
CoreX Project Generator
Generates Django projects from templates
"""

import os
from pathlib import Path
from typing import Dict

from .base_generator import BaseGenerator
from ..utils import (
    create_directory,
    get_template_path,
    print_error,
    print_info,
    print_success,
    print_warning,
    generate_secret_key,
    scan_project_for_unresolved_placeholders,
)


class ProjectGenerator(BaseGenerator):
    """Generator for Django projects"""
    
    def __init__(self):
        super().__init__("projects")
    
    def generate(self, output_path: Path, context: Dict) -> bool:
        """Generate a complete Django project"""
        try:
            # Create project directory
            create_directory(output_path)
            
            # Generate project structure
            self._generate_project_structure(output_path, context)
            
            # Generate configuration files
            self._generate_config_files(output_path, context)
            
            # Generate Docker files if requested
            if context.get("docker", False):
                self._generate_docker_files(output_path, context)
            
            # Generate UI files if requested
            if context.get("ui", "none") != "none":
                self._generate_ui_files(output_path, context)
            
            # Generate API files if requested
            if context.get("api", False):
                self._generate_api_files(output_path, context)
            
            print_success(f"Project '{context['project_name']}' generated successfully")
            return True
            
        except Exception as e:
            print_error(f"Failed to generate project: {e}")
            return False
    
    def _generate_project_structure(self, project_path: Path, context: Dict) -> None:
        """Generate basic project structure"""
        project_name = context["project_name"]
        main_project_dir = project_path / project_name
        create_directory(main_project_dir)
        
        # Create manage.py
        manage_content = self._render_template("manage.py.j2", context)
        self._write_file(project_path / "manage.py", manage_content)
        
        # Create main project files
        main_files = [
            "settings.py",
            "urls.py",
            "wsgi.py",
            "asgi.py",
        ]
        
        for filename in main_files:
            content = self._render_template(f"{filename}.j2", context)
            self._write_file(main_project_dir / filename, content)
        
        # Create __init__.py files
        (main_project_dir / "__init__.py").touch()
        
        # Create static and media directories
        static_dir = project_path / "static"
        media_dir = project_path / "media"
        create_directory(static_dir)
        create_directory(media_dir)
        
        # Create CSS directory
        css_dir = static_dir / "css"
        create_directory(css_dir)
        
        # Create templates directory
        templates_dir = project_path / "templates"
        create_directory(templates_dir)
        
        # Create base template
        base_content = self._render_template("base.html.j2", context)
        self._write_file(templates_dir / "base.html", base_content)
        
        # Create logs directory
        logs_dir = project_path / "logs"
        create_directory(logs_dir)
        (logs_dir / ".gitkeep").touch()
    
    def _generate_config_files(self, project_path: Path, context: Dict) -> None:
        """Generate configuration files"""
        # Generate pyproject.toml
        pyproject_content = self._render_template("pyproject.toml.j2", context)
        self._write_file(project_path / "pyproject.toml", pyproject_content)

        # Generate README.md
        readme_content = self._render_template("README.md.j2", context)
        self._write_file(project_path / "README.md", readme_content)

        # Generate .env file with secure SECRET_KEY
        # Ensure SECRET_KEY is generated securely if not provided
        if 'SECRET_KEY' not in context:
            context['SECRET_KEY'] = generate_secret_key()

        env_content = self._render_template("env.j2", context)
        self._write_file(project_path / ".env", env_content)

        # Generate .env.example with warnings and safe defaults
        env_example = []
        env_example.append("# Example environment configuration for production")
        env_example.append("# IMPORTANT: Copy to .env and set secure values before deploying")
        env_example.append(f"SECRET_KEY={context['SECRET_KEY']}")
        env_example.append("DEBUG=False")
        env_example.append("ALLOWED_HOSTS=yourdomain.com,127.0.0.1")

        if context.get('database') == 'postgres':
            env_example += [
                f"DB_NAME={context['project_name']}",
                "DB_USER=postgres",
                "DB_PASSWORD=CHANGE_ME",
                "DB_HOST=localhost",
                "DB_PORT=5432",
            ]
        elif context.get('database') == 'mysql':
            env_example += [
                f"DB_NAME={context['project_name']}",
                "DB_USER=root",
                "DB_PASSWORD=CHANGE_ME",
                "DB_HOST=localhost",
                "DB_PORT=3306",
            ]

        env_example.append("# Example: REDIS_URL=redis://127.0.0.1:6379/1")
        self._write_file(project_path / ".env.example", "\n".join(env_example))

        # Generate requirements.txt (fallback)
        requirements_content = self._render_template("requirements.txt.j2", context)
        self._write_file(project_path / "requirements.txt", requirements_content)

        # Quick check for unresolved templates and warn
        try:
            findings = scan_project_for_unresolved_placeholders(project_path)
            if findings:
                print_warning("Detected unresolved Jinja2 placeholders in generated project:")
                for path, placeholders in findings:
                    print_warning(f" - {path}: {placeholders}")
        except Exception:
            # Non-fatal
            pass
    
    def _generate_docker_files(self, project_path: Path, context: Dict) -> None:
        """Generate Docker configuration files"""
        docker_files = [
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.prod.yml",
            ".dockerignore",
        ]
        
        for filename in docker_files:
            content = self._render_template(f"{filename}.j2", context)
            self._write_file(project_path / filename, content)
    
    def _generate_ui_files(self, project_path: Path, context: Dict) -> None:
        """Generate UI framework files"""
        ui = context["ui"]
        
        if ui == "tailwind":
            # Generate Tailwind configuration
            tailwind_files = [
                "tailwind.config.js",
                "package.json",
            ]
            
            for filename in tailwind_files:
                content = self._render_template(f"ui/tailwind/{filename}.j2", context)
                self._write_file(project_path / filename, content)
            
            # Create CSS directory and input file
            css_dir = project_path / "static" / "css"
            create_directory(css_dir)
            
            # Generate main CSS file
            css_content = self._render_template("ui/tailwind/input.css.j2", context)
            self._write_file(css_dir / "input.css", css_content)
            
            # Generate a basic compiled CSS file for immediate use
            output_css_content = """/* Basic CSS for immediate use - replace with compiled Tailwind */

/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f9fafb;
}

/* Utility classes */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.text-center { text-align: center; }
.text-3xl { font-size: 1.875rem; font-weight: bold; }
.text-xl { font-size: 1.25rem; font-weight: 600; }
.text-blue-600 { color: #2563eb; }
.text-blue-800 { color: #1e40af; }
.text-gray-600 { color: #4b5563; }
.text-gray-700 { color: #374151; }
.text-gray-900 { color: #111827; }
.text-gray-500 { color: #6b7280; }

.bg-white { background-color: white; }
.bg-gray-50 { background-color: #f9fafb; }
.bg-blue-100 { background-color: #dbeafe; }
.bg-blue-800 { background-color: #1e40af; }

.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.py-2 { padding: 0.5rem 0; }
.py-6 { padding: 1.5rem 0; }
.py-8 { padding: 2rem 0; }
.px-2 { padding: 0 0.5rem; }
.px-4 { padding: 0 1rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-8 { margin-bottom: 2rem; }
.mt-8 { margin-top: 2rem; }

.min-h-screen { min-height: 100vh; }
.max-w-7xl { max-width: 80rem; }
.mx-auto { margin: 0 auto; }

.flex { display: flex; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.items-center { align-items: center; }
.space-x-4 > * + * { margin-left: 1rem; }
.space-x-2 > * + * { margin-left: 0.5rem; }

.grid { display: grid; }
.gap-6 { gap: 1.5rem; }

.h-16 { height: 4rem; }
.h-96 { height: 24rem; }

.border { border: 1px solid #d1d5db; }
.border-4 { border: 4px solid; }
.border-dashed { border-style: dashed; }
.border-gray-200 { border-color: #e5e7eb; }
.border-gray-300 { border-color: #d1d5db; }
.border-blue-500 { border-color: #3b82f6; }

.rounded { border-radius: 0.25rem; }
.rounded-lg { border-radius: 0.5rem; }

.shadow { box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); }
.shadow-md { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }

/* Navigation */
nav {
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Card component */
.card {
    background: white;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Links */
a {
    color: #2563eb;
    text-decoration: none;
}

a:hover {
    color: #1e40af;
    text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        padding: 0 0.5rem;
    }
    
    .text-3xl {
        font-size: 1.5rem;
    }
}"""
            self._write_file(css_dir / "output.css", output_css_content)
            
            # Create theme app for django-tailwind
            theme_dir = project_path / "theme"
            create_directory(theme_dir)
            (theme_dir / "__init__.py").touch()
            
            # Create theme apps.py
            theme_apps_content = f"""from django.apps import AppConfig

class ThemeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'theme'
"""
            self._write_file(theme_dir / "apps.py", theme_apps_content)
        
        elif ui == "bootstrap":
            # Generate Bootstrap configuration
            bootstrap_files = [
                "package.json",
            ]
            
            for filename in bootstrap_files:
                content = self._render_template(f"ui/bootstrap/{filename}.j2", context)
                self._write_file(project_path / filename, content)
                
            # Create custom CSS file for Bootstrap customization
            css_dir = project_path / "static" / "css"
            create_directory(css_dir)
            bootstrap_css_content = """/* Bootstrap 5 Customizations */

:root {
  --bs-primary: #007bff;
  --bs-secondary: #6c757d;
}

.btn-custom {
  background-color: var(--bs-primary);
  border-color: var(--bs-primary);
  color: white;
}

.btn-custom:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.navbar-brand {
  font-weight: bold;
}
"""
            self._write_file(css_dir / "style.css", bootstrap_css_content)
    
    def _generate_api_files(self, project_path: Path, context: Dict) -> None:
        """Generate API-related files"""
        # Create API directory
        api_dir = project_path / "api"
        create_directory(api_dir)
        
        # Generate API files
        api_files = [
            "urls.py",
            "serializers.py",
            "views.py",
        ]
        
        for filename in api_files:
            content = self._render_template(f"api/{filename}.j2", context)
            self._write_file(api_dir / filename, content)
        
        (api_dir / "__init__.py").touch()