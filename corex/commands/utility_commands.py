"""
CoreX Utility Commands
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.table import Table

from ..utils import (
    get_project_root,
    print_error,
    print_info,
    print_step,
    print_success,
    print_warning,
    run_command,
    check_dependencies,
    validate_project_name,
    create_file_tree,
)
from .. import generators

console = Console()


def test_command(
    ctx: click.Context,
    app_name: Optional[str],
    coverage: bool,
    parallel: bool,
) -> None:
    """Run Django tests"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    os.chdir(project_root)
    
    # Build test command
    if coverage:
        # Check if coverage is installed
        code, _, _ = run_command("python3 -c 'import coverage'", capture_output=True)
        if code != 0:
            print_info("Installing coverage...")
            run_command("pip install coverage", capture_output=True)
        
        cmd = "coverage run --source='.' manage.py test"
    else:
        cmd = "python3 manage.py test"
    
    if app_name:
        cmd += f" {app_name}"
    
    if parallel:
        cmd += " --parallel"
    
    print_info("Running tests...")
    code, stdout, stderr = run_command(cmd)
    
    if code == 0:
        print_success("Tests passed!")
        
        if coverage:
            print_info("Generating coverage report...")
            run_command("coverage report")
            
            # Generate HTML coverage report
            code_html, _, _ = run_command("coverage html", capture_output=True)
            if code_html == 0:
                print_success("Coverage HTML report generated at htmlcov/index.html")
    else:
        print_error("Tests failed!")
        if stderr:
            console.print(f"[red]{stderr}[/red]")


def doctor_command(ctx: click.Context, fix: bool) -> None:
    """Check environment health and diagnose issues"""
    print_step(1, 6, "Checking environment...")
    
    # Check dependencies
    deps = check_dependencies()
    
    # Create results table
    table = Table(title="Environment Health Check")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Notes", style="dim")
    
    for name, installed in deps.items():
        status = "✓ Installed" if installed else "✗ Missing"
        style = "green" if installed else "red"
        notes = ""
        
        if installed:
            # Get version
            if name == "python":
                import sys
                version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            else:
                code, stdout, _ = run_command(f"{name} --version", capture_output=True)
                if code == 0:
                    version = stdout.strip().split('\n')[0]
                else:
                    version = "Unknown"
        else:
            version = "N/A"
            if name == "poetry":
                notes = "Install: curl -sSL https://install.python-poetry.org | python3 -"
            elif name == "docker":
                notes = "Install: https://docs.docker.com/get-docker/"
            elif name == "git":
                notes = "Install: https://git-scm.com/downloads"
        
        table.add_row(name.title(), status, version, notes)
    
    console.print(table)
    
    # Check Django project
    print_step(2, 6, "Checking Django project...")
    project_root = get_project_root()
    issues = []
    
    if project_root:
        print_success(f"Django project found at: {project_root}")
        
        # Check for common issues
        # Check manage.py
        if not (project_root / "manage.py").exists():
            issues.append("Missing manage.py")
        
        # Check settings
        settings_files = list(project_root.glob("**/settings.py"))
        if not settings_files:
            issues.append("No settings.py found")
        
        # Check requirements
        has_poetry = (project_root / "pyproject.toml").exists()
        has_requirements = (project_root / "requirements.txt").exists()
        if not has_poetry and not has_requirements:
            issues.append("No dependency management file found")
        
        # Check .env file
        if not (project_root / ".env").exists():
            issues.append("Missing .env file (recommended for environment variables)")
        
        # Check static/media directories
        if not (project_root / "static").exists():
            issues.append("Missing static directory")
        if not (project_root / "media").exists():
            issues.append("Missing media directory")
        
        if issues:
            print_warning("Found issues:")
            for issue in issues:
                print_warning(f"  • {issue}")
        else:
            print_success("Django project structure looks healthy")
    else:
        print_warning("No Django project found in current directory")
    
    # Check database
    print_step(3, 6, "Checking database...")
    if project_root:
        os.chdir(project_root)
        code, stdout, stderr = run_command("python3 manage.py check --database default", capture_output=True)
        if code == 0:
            print_success("Database configuration is valid")
        else:
            print_error(f"Database issues found: {stderr}")
            issues.append(f"Database error: {stderr}")
    
    # Check migrations
    print_step(4, 6, "Checking migrations...")
    if project_root:
        code, stdout, stderr = run_command("python3 manage.py showmigrations", capture_output=True)
        if code == 0:
            if "[ ]" in stdout:
                print_warning("Unapplied migrations found")
                issues.append("Unapplied migrations")
            else:
                print_success("All migrations are up to date")
        else:
            print_warning(f"Migration check failed: {stderr}")
    
    # Check static files
    print_step(5, 6, "Checking static files...")
    if project_root:
        staticfiles_dir = project_root / "staticfiles"
        if not staticfiles_dir.exists():
            print_warning("Static files not collected")
            issues.append("Static files not collected")
        else:
            print_success("Static files collected")
    
    # Summary
    print_step(6, 6, "Health check summary")
    if not issues:
        print_success("🎉 Your project appears to be healthy!")
    else:
        print_warning(f"Found {len(issues)} issue(s) that may need attention")
    
    # Auto-fix if requested
    if fix and issues and project_root:
        print_info("🔧 Attempting to fix issues...")
        
        if "Missing .env file (recommended for environment variables)" in issues:
            env_content = """# Environment Configuration\nSECRET_KEY=your-secret-key-here\nDEBUG=True\nALLOWED_HOSTS=localhost,127.0.0.1\n"""
            (project_root / ".env").write_text(env_content)
            print_success("Created .env file")
        
        if "Missing static directory" in issues:
            (project_root / "static").mkdir(exist_ok=True)
            print_success("Created static directory")
        
        if "Missing media directory" in issues:
            (project_root / "media").mkdir(exist_ok=True)
            print_success("Created media directory")
        
        if "Unapplied migrations" in issues:
            print_info("Applying migrations...")
            code, _, stderr = run_command("python3 manage.py migrate", capture_output=True)
            if code == 0:
                print_success("Migrations applied")
            else:
                print_error(f"Failed to apply migrations: {stderr}")
        
        if "Static files not collected" in issues:
            print_info("Collecting static files...")
            code, _, stderr = run_command("python3 manage.py collectstatic --noinput", capture_output=True)
            if code == 0:
                print_success("Static files collected")
            else:
                print_warning(f"Failed to collect static files: {stderr}")


def seed_command(
    ctx: click.Context,
    app: Optional[str],
    count: int,
) -> None:
    """Generate demo data for apps"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    if app:
        # Check if app exists
        app_path = project_root / app
        if not app_path.exists():
            print_error(f"App '{app}' does not exist")
            return
        
        # Check if app has a seed command
        seed_command_path = app_path / "management" / "commands" / "seed.py"
        if seed_command_path.exists():
            print_info(f"Running seed command for {app}...")
            cmd = f"python3 manage.py seed --app {app} --count {count}"
        else:
            print_warning(f"No seed command found for app '{app}'")
            print_info("Generating basic seed data...")
            cmd = f"python3 manage.py seed --count {count}"
    else:
        print_info("Generating seed data for all apps...")
        cmd = f"python3 manage.py seed --count {count}"
    
    # Check if seed command exists in Django
    code, _, stderr = run_command("python3 manage.py help seed", capture_output=True)
    if code != 0:
        print_warning("Django seed command not found")
        print_info("Creating basic seed data script...")
        
        # Create a basic seed script
        seed_script = f"""#!/usr/bin/env python
# Basic seed data generator
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_root.name}.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

print("Generating seed data...")

# Create test users
for i in range({count}):
    username = fake.user_name()
    email = fake.email()
    
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            password='demo123',  # Default demo password
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        print(f"Created user: {{user.username}}")

print("Seed data generation complete!")
"""
        
        seed_file = project_root / "seed_data.py"
        seed_file.write_text(seed_script)
        
        # Install faker if not available
        print_info("Installing faker for data generation...")
        run_command("pip install faker", capture_output=True)
        
        # Run the seed script
        code, stdout, stderr = run_command("python3 seed_data.py")
        if code == 0:
            print_success("Seed data generated successfully!")
        else:
            print_error(f"Failed to generate seed data: {stderr}")
    else:
        print_info(f"Running: {cmd}")
        code, stdout, stderr = run_command(cmd)
        if code == 0:
            print_success("Seed data generated successfully!")
        else:
            print_error(f"Failed to generate seed data: {stderr}")
