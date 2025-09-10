"""
CoreX generators - Template-based code generation
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template

from .utils import (
    create_directory,
    get_template_path,
    print_error,
    print_info,
    print_success,
    print_warning,
)


def generate_project(
    project_path: Path,
    project_name: str,
    auth: str,
    ui: str,
    database: str,
    docker: bool,
    api: bool,
) -> bool:
    """Generate a complete Django project"""
    try:
        # Create project directory
        create_directory(project_path)
        
        # Get templates directory
        templates_dir = get_template_path("projects")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Project context
        context = {
            "project_name": project_name,
            "auth": auth,
            "ui": ui,
            "database": database,
            "docker": docker,
            "api": api,
            "python_version": "3.9",
        }
        
        # Generate project structure
        generate_project_structure(project_path, context, env)
        
        # Generate configuration files
        generate_config_files(project_path, context, env)
        
        # Generate Docker files if requested
        if docker:
            generate_docker_files(project_path, context, env)
        
        # Generate UI files if requested
        if ui != "none":
            generate_ui_files(project_path, context, env)
        
        # Generate API files if requested
        if api:
            generate_api_files(project_path, context, env)
        
        print_success(f"Project '{project_name}' generated successfully")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate project: {e}")
        return False


def generate_project_structure(project_path: Path, context: Dict, env: Environment) -> None:
    """Generate basic project structure"""
    project_name = context["project_name"]
    main_project_dir = project_path / project_name
    create_directory(main_project_dir)
    
    # Create manage.py
    manage_template = env.get_template("manage.py.j2")
    manage_content = manage_template.render(**context)
    (project_path / "manage.py").write_text(manage_content)
    
    # Create main project files
    main_files = [
        "settings.py",
        "urls.py",
        "wsgi.py",
        "asgi.py",
    ]
    
    for filename in main_files:
        template = env.get_template(f"{filename}.j2")
        content = template.render(**context)
        (main_project_dir / filename).write_text(content)
    
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
    base_template = env.get_template("base.html.j2")
    base_content = base_template.render(**context)
    (templates_dir / "base.html").write_text(base_content)
    
    # Create logs directory
    logs_dir = project_path / "logs"
    create_directory(logs_dir)
    (logs_dir / ".gitkeep").touch()


def generate_config_files(project_path: Path, context: Dict, env: Environment) -> None:
    """Generate configuration files"""
    # Generate pyproject.toml
    pyproject_template = env.get_template("pyproject.toml.j2")
    pyproject_content = pyproject_template.render(**context)
    (project_path / "pyproject.toml").write_text(pyproject_content)
    
    # Generate README.md
    readme_template = env.get_template("README.md.j2")
    readme_content = readme_template.render(**context)
    (project_path / "README.md").write_text(readme_content)
    
    # Generate .env file
    env_template = env.get_template("env.j2")
    env_content = env_template.render(**context)
    (project_path / ".env").write_text(env_content)
    
    # Generate requirements.txt (fallback)
    requirements_template = env.get_template("requirements.txt.j2")
    requirements_content = requirements_template.render(**context)
    (project_path / "requirements.txt").write_text(requirements_content)


def generate_docker_files(project_path: Path, context: Dict, env: Environment) -> None:
    """Generate Docker configuration files"""
    docker_files = [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.prod.yml",
        ".dockerignore",
    ]
    
    for filename in docker_files:
        template = env.get_template(f"{filename}.j2")
        content = template.render(**context)
        (project_path / filename).write_text(content)


def generate_ui_files(project_path: Path, context: Dict, env: Environment) -> None:
    """Generate UI framework files"""
    ui = context["ui"]
    
    if ui == "tailwind":
        # Generate Tailwind configuration
        tailwind_files = [
            "tailwind.config.js",
            "package.json",
        ]
        
        for filename in tailwind_files:
            template = env.get_template(f"ui/tailwind/{filename}.j2")
            content = template.render(**context)
            (project_path / filename).write_text(content)
        
        # Create CSS directory and input file
        css_dir = project_path / "static" / "css"
        create_directory(css_dir)
        
        # Generate main CSS file
        css_template = env.get_template("ui/tailwind/input.css.j2")
        css_content = css_template.render(**context)
        (css_dir / "input.css").write_text(css_content)
        
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
        (css_dir / "output.css").write_text(output_css_content)
        
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
        (theme_dir / "apps.py").write_text(theme_apps_content)
    
    elif ui == "bootstrap":
        # Generate Bootstrap configuration
        bootstrap_files = [
            "package.json",
        ]
        
        for filename in bootstrap_files:
            template = env.get_template(f"ui/bootstrap/{filename}.j2")
            content = template.render(**context)
            (project_path / filename).write_text(content)
            
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
        (css_dir / "style.css").write_text(bootstrap_css_content)


def generate_api_files(project_path: Path, context: Dict, env: Environment) -> None:
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
        template = env.get_template(f"api/{filename}.j2")
        content = template.render(**context)
        (api_dir / filename).write_text(content)
    
    (api_dir / "__init__.py").touch()


def generate_app(
    project_root: Path,
    app_name: str,
    app_type: Optional[str],
    auth: Optional[str],
    ui: Optional[str],
    seed: bool,
    api: bool,
) -> bool:
    """Generate a Django app with CoreX"""
    try:
        # Get templates directory
        templates_dir = get_template_path("apps")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # App context
        context = {
            "app_name": app_name,
            "app_type": app_type,
            "auth": auth,
            "ui": ui,
            "seed": seed,
            "api": api,
        }
        
        # Create app directory
        app_path = project_root / app_name
        create_directory(app_path)
        
        # Generate app structure
        generate_app_structure(app_path, context, env)
        
        # Generate app-specific files based on type
        if app_type:
            generate_app_type_files(app_path, app_type, context, env)
        
        # Generate seed data if requested
        if seed:
            generate_seed_data(app_path, app_type, context, env)
        
        print_success(f"App '{app_name}' generated successfully")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate app: {e}")
        return False


def generate_app_structure(app_path: Path, context: Dict, env: Environment) -> None:
    """Generate basic app structure"""
    app_name = context["app_name"]
    
    # Create __init__.py
    (app_path / "__init__.py").touch()
    
    # Create apps.py
    apps_template = env.get_template("apps.py.j2")
    apps_content = apps_template.render(**context)
    (app_path / "apps.py").write_text(apps_content)
    
    # Create models.py
    models_template = env.get_template("models.py.j2")
    models_content = models_template.render(**context)
    (app_path / "models.py").write_text(models_content)
    
    # Create views.py
    views_template = env.get_template("views.py.j2")
    views_content = views_template.render(**context)
    (app_path / "views.py").write_text(views_content)
    
    # Create urls.py
    urls_template = env.get_template("urls.py.j2")
    urls_content = urls_template.render(**context)
    (app_path / "urls.py").write_text(urls_content)
    
    # Create admin.py
    admin_template = env.get_template("admin.py.j2")
    admin_content = admin_template.render(**context)
    (app_path / "admin.py").write_text(admin_content)
    
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
        template = env.get_template(f"tests/{filename}.j2")
        content = template.render(**context)
        (tests_dir / filename).write_text(content)
    
    # Create migrations directory
    migrations_dir = app_path / "migrations"
    create_directory(migrations_dir)
    (migrations_dir / "__init__.py").touch()
    
    # Create templates directory if UI is enabled
    if context["ui"] != "none":
        templates_dir = app_path / "templates" / app_name
        create_directory(templates_dir)
        
        # Generate templates
        template_files = [
            "list.html",
            "detail.html",
            "form.html",
        ]
        
        for filename in template_files:
            template = env.get_template(f"templates/{filename}.j2")
            content = template.render(**context)
            (templates_dir / filename).write_text(content)
    
    # Create API files if API is enabled
    if context["api"]:
        api_dir = app_path / "api"
        create_directory(api_dir)
        (api_dir / "__init__.py").touch()
        
        api_files = [
            "serializers.py",
            "views.py",
            "urls.py",
        ]
        
        for filename in api_files:
            template = env.get_template(f"api/{filename}.j2")
            content = template.render(**context)
            (api_dir / filename).write_text(content)


def generate_app_type_files(app_path: Path, app_type: str, context: Dict, env: Environment) -> None:
    """Generate app-specific files based on type"""
    try:
        # Get app-specific template
        template = env.get_template(f"types/{app_type}.py.j2")
        content = template.render(**context)
        
        # Replace the main models.py file with app-specific models
        models_file = app_path / "models.py"
        
        # Replace the entire content with app-specific models
        models_file.write_text(content)
        
        print_info(f"Generated {app_type}-specific models")
        
    except Exception as e:
        print_warning(f"Could not generate {app_type}-specific files: {e}")


def generate_seed_data(app_path: Path, app_type: Optional[str], context: Dict, env: Environment) -> None:
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
        seed_template = env.get_template("management/seed.py.j2")
        seed_content = seed_template.render(**context)
        (commands_dir / "seed.py").write_text(seed_content)
        
        print_info("Generated seed data command")
        
    except Exception as e:
        print_warning(f"Could not generate seed data: {e}")


def generate_scaffold(
    project_root: Path,
    app_name: str,
    feature: str,
    model: Optional[str],
    fields: Optional[str],
) -> bool:
    """Generate scaffold for existing app"""
    try:
        app_path = project_root / app_name
        
        # Get templates directory
        templates_dir = get_template_path("scaffold")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Parse fields if provided
        field_list = []
        if fields:
            field_list = parse_fields(fields)
        
        # Scaffold context
        context = {
            "app_name": app_name,
            "feature": feature,
            "model": model,
            "fields": field_list,
        }
        
        # Generate scaffold based on feature
        if feature == "model":
            generate_model_scaffold(app_path, context, env)
        elif feature == "view":
            generate_view_scaffold(app_path, context, env)
        elif feature == "form":
            generate_form_scaffold(app_path, context, env)
        elif feature == "api":
            generate_api_scaffold(app_path, context, env)
        else:
            print_warning(f"Unknown scaffold feature: {feature}")
            return False
        
        print_success(f"Scaffold '{feature}' generated successfully")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate scaffold: {e}")
        return False


def parse_fields(fields_str: str) -> List[Dict]:
    """Parse field definitions from string"""
    fields = []
    
    for field_def in fields_str.split(','):
        parts = field_def.strip().split(':')
        if len(parts) >= 2:
            field = {
                "name": parts[0].strip(),
                "type": parts[1].strip(),
                "options": parts[2].strip() if len(parts) > 2 else "",
            }
            fields.append(field)
    
    return fields


def generate_model_scaffold(app_path: Path, context: Dict, env: Environment) -> None:
    """Generate model scaffold"""
    if not context["model"]:
        print_error("Model name is required for model scaffold")
        return
    
    # Generate model file
    template = env.get_template("model.py.j2")
    content = template.render(**context)
    
    # Read existing models.py content
    models_file = app_path / "models.py"
    if models_file.exists():
        existing_content = models_file.read_text()
        # Append new model to existing content
        updated_content = existing_content.rstrip() + "\n\n" + content
        models_file.write_text(updated_content)
    else:
        # Create new models.py if it doesn't exist
        models_file.write_text(content)


def generate_view_scaffold(app_path: Path, context: Dict, env: Environment) -> None:
    """Generate view scaffold"""
    template = env.get_template("view.py.j2")
    content = template.render(**context)
    
    # Read existing views.py content and append safely
    views_file = app_path / "views.py"
    if views_file.exists():
        existing_content = views_file.read_text()
        # Append new view to existing content
        updated_content = existing_content.rstrip() + "\n\n" + content
        views_file.write_text(updated_content)
    else:
        # Create new views.py if it doesn't exist
        views_file.write_text(content)


def generate_form_scaffold(app_path: Path, context: Dict, env: Environment) -> None:
    """Generate form scaffold"""
    forms_file = app_path / "forms.py"
    
    # Create forms.py with header if it doesn't exist
    if not forms_file.exists():
        forms_file.write_text("# Forms\n\n")
    
    template = env.get_template("form.py.j2")
    content = template.render(**context)
    
    # Read existing content and append safely
    existing_content = forms_file.read_text()
    updated_content = existing_content.rstrip() + "\n\n" + content
    forms_file.write_text(updated_content)


def generate_api_scaffold(app_path: Path, context: Dict, env: Environment) -> None:
    """Generate API scaffold"""
    api_dir = app_path / "api"
    if not api_dir.exists():
        create_directory(api_dir)
        (api_dir / "__init__.py").touch()
    
    # Generate API files
    api_files = [
        "serializer.py",
        "view.py",
        "url.py",
    ]
    
    for filename in api_files:
        template = env.get_template(f"api/{filename}.j2")
        content = template.render(**context)
        
        # Handle existing files or create new ones safely
        file_path = api_dir / filename
        if file_path.exists():
            existing_content = file_path.read_text()
            updated_content = existing_content.rstrip() + "\n\n" + content
            file_path.write_text(updated_content)
        else:
            file_path.write_text(content)


def generate_ci_pipeline(project_root: Path, github: bool, gitlab: bool, docker: bool) -> bool:
    """Generate CI/CD pipeline configuration"""
    try:
        # Get templates directory
        templates_dir = get_template_path("ci")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # CI context
        context = {
            "docker": docker,
            "python_version": "3.9",
        }
        
        if github:
            # Create GitHub Actions directory
            github_dir = project_root / ".github" / "workflows"
            create_directory(github_dir)
            
            # Generate GitHub Actions workflow
            workflow_template = env.get_template("github-actions.yml.j2")
            workflow_content = workflow_template.render(**context)
            (github_dir / "ci.yml").write_text(workflow_content)
        
        if gitlab:
            # Generate GitLab CI configuration
            gitlab_template = env.get_template(".gitlab-ci.yml.j2")
            gitlab_content = gitlab_template.render(**context)
            (project_root / ".gitlab-ci.yml").write_text(gitlab_content)
        
        return True
        
    except Exception as e:
        print_error(f"Failed to generate CI pipeline: {e}")
        return False


def generate_integration(project_root: Path, service: str, config: Optional[str]) -> bool:
    """Generate integration files for external services"""
    try:
        # Get templates directory
        templates_dir = get_template_path("integrations")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Integration context
        context = {
            "service": service,
            "config": config,
        }
        
        # Generate service-specific files
        service_files = [
            "settings.py",
            "views.py",
            "urls.py",
        ]
        
        for filename in service_files:
            try:
                template = env.get_template(f"{service}/{filename}.j2")
                content = template.render(**context)
                
                # Create integration directory
                integration_dir = project_root / "integrations" / service
                create_directory(integration_dir)
                
                # Write file
                (integration_dir / filename).write_text(content)
                
            except Exception as e:
                print_warning(f"Could not generate {filename} for {service}: {e}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to generate integration: {e}")
        return False


def generate_deployment(
    project_root: Path,
    platform: str,
    env_file: str,
    auto_db: bool,
    domain: Optional[str],
    region: Optional[str],
) -> bool:
    """Generate deployment configuration for various platforms"""
    try:
        # Get templates directory
        templates_dir = get_template_path("deployment")
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Deployment context
        context = {
            "platform": platform,
            "project_name": project_root.name,
            "env_file": env_file,
            "auto_db": auto_db,
            "domain": domain,
            "region": region,
            "python_version": "3.9",
        }
        
        # Generate platform-specific files
        platform_files = get_platform_files(platform)
        
        for filename in platform_files:
            try:
                template = env.get_template(f"{platform}/{filename}.j2")
                content = template.render(**context)
                
                # Write file to project root
                (project_root / filename).write_text(content)
                print_info(f"Generated {filename} for {platform}")
                
            except Exception as e:
                print_warning(f"Could not generate {filename} for {platform}: {e}")
        
        # Generate common deployment files if they don't exist
        generate_common_deployment_files(project_root, context)
        
        print_success(f"Deployment configuration for {platform} generated successfully")
        return True
        
    except Exception as e:
        print_error(f"Failed to generate deployment configuration: {e}")
        return False


def get_platform_files(platform: str) -> List[str]:
    """Get list of files to generate for each platform"""
    platform_files = {
        "vercel": ["vercel.json", "requirements.txt"],
        "railway": ["railway.toml", "Procfile"],
        "render": ["render.yaml", "build.sh"],
        "heroku": ["Procfile", "runtime.txt", "release.sh"],
    }
    
    return platform_files.get(platform, [])


def generate_common_deployment_files(project_root: Path, context: Dict) -> None:
    """Generate common deployment files if they don't exist"""
    # Generate Dockerfile if it doesn't exist
    dockerfile_path = project_root / "Dockerfile"
    if not dockerfile_path.exists():
        dockerfile_content = f"""# Dockerfile for {context['project_name']}
FROM python:{context['python_version']}-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "{context['project_name']}.wsgi:application", "--bind", "0.0.0.0:8000"]
"""
        dockerfile_path.write_text(dockerfile_content)
        print_info("Generated Dockerfile")
    
    # Generate docker-compose.yml if it doesn't exist
    docker_compose_path = project_root / "docker-compose.yml"
    if not docker_compose_path.exists():
        docker_compose_content = f"""version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB={context['project_name']}
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
"""
        docker_compose_path.write_text(docker_compose_content)
        print_info("Generated docker-compose.yml")
    
    # Update requirements.txt with deployment dependencies
    requirements_path = project_root / "requirements.txt"
    if requirements_path.exists():
        content = requirements_path.read_text()
        deployment_deps = [
            "gunicorn>=20.1.0",
            "psycopg2-binary>=2.9.0",
            "whitenoise>=6.0.0",
            "dj-database-url>=1.0.0",
        ]
        
        for dep in deployment_deps:
            if dep.split(">=")[0] not in content:
                content += f"\n{dep}"
        
        requirements_path.write_text(content)
        print_info("Updated requirements.txt with deployment dependencies")
