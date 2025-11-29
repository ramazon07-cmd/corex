"""
CoreX generators - Template-based code generation
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .generators.generator_factory import GeneratorFactory
from .utils import (
    create_directory,
    get_template_path,
    print_error,
    print_info,
    print_success,
    print_warning,
    generate_secret_key,
    scan_project_for_unresolved_placeholders,
)


# Create a global factory instance
_factory = GeneratorFactory()


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
    # Create project generator
    generator = _factory.create_project_generator()
    
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
    
    return generator.generate(project_path, context)


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
    # Create app generator
    generator = _factory.create_app_generator()
    
    # App context
    context = {
        "app_name": app_name,
        "app_type": app_type,
        "auth": auth,
        "ui": ui,
        "seed": seed,
        "api": api,
    }
    
    app_path = project_root / app_name
    return generator.generate(app_path, context)


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
        from jinja2 import Environment, FileSystemLoader
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


def generate_model_scaffold(app_path: Path, context: Dict, env) -> None:
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


def generate_view_scaffold(app_path: Path, context: Dict, env) -> None:
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


def generate_form_scaffold(app_path: Path, context: Dict, env) -> None:
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


def generate_api_scaffold(app_path: Path, context: Dict, env) -> None:
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
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(templates_dir))

        # CI context
        context = {
            "docker": docker,
            "python_version": "3.9",
            "database": "postgres",  # Default for CI
            "project_name": project_root.name,
        }

        if github:
            # Create GitHub Actions directory
            github_dir = project_root / ".github" / "workflows"
            create_directory(github_dir)

            # Generate GitHub Actions workflow
            workflow_template = env.get_template("github-actions.yml.j2")
            workflow_content = workflow_template.render(**context)
            (github_dir / "ci.yml").write_text(workflow_content)

            # Add a small wrapper that runs corex new and validates
            print_info("Generated GitHub Actions workflow for CI")

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
        from jinja2 import Environment, FileSystemLoader
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
        from jinja2 import Environment, FileSystemLoader
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