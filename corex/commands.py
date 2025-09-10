"""
CoreX command implementations
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .generators import (
    generate_app,
    generate_ci_pipeline,
    generate_deployment,
    generate_integration,
    generate_project,
    generate_scaffold,
)
from .utils import (
    check_dependencies,
    create_gitignore,
    ensure_git_repo,
    format_duration,
    get_project_root,
    print_error,
    print_info,
    print_step,
    print_success,
    print_warning,
    run_command,
    show_progress_spinner,
    validate_project_name,
)

console = Console()


def new_command(
    ctx: click.Context,
    project_name: str,
    auth: str,
    ui: str,
    database: str,
    docker: bool,
    api: bool,
) -> None:
    """Create a new Django project with CoreX"""
    start_time = time.time()
    
    # Validate project name
    if not validate_project_name(project_name):
        print_error(f"Invalid project name: {project_name}")
        print_info("Project name must be a valid Python identifier (no spaces, starts with letter)")
        return
    
    # Check if project directory already exists
    project_path = Path.cwd() / project_name
    if project_path.exists():
        print_error(f"Directory '{project_name}' already exists")
        return
    
    # Check dependencies
    print_step(1, 8, "Checking dependencies...")
    deps = check_dependencies()
    
    missing_deps = [name for name, installed in deps.items() if not installed]
    if missing_deps:
        print_warning(f"Missing dependencies: {', '.join(missing_deps)}")
        print_info("Some features may not work without these dependencies")
    
    # Create project
    print_step(2, 8, f"Creating Django project '{project_name}'...")
    success = generate_project(project_path, project_name, auth, ui, database, docker, api)
    
    if not success:
        print_error("Failed to create project")
        return
    
    # Initialize git repository
    print_step(3, 8, "Initializing git repository...")
    ensure_git_repo(project_path)
    
    # Create .gitignore
    print_step(4, 8, "Creating .gitignore...")
    create_gitignore(project_path)
    
    # Install dependencies
    print_step(5, 8, "Installing dependencies...")
    os.chdir(project_path)
    
    if deps["poetry"]:
        code, _, stderr = run_command("poetry install", capture_output=True)
        if code == 0:
            print_success("Dependencies installed with Poetry")
        else:
            print_warning(f"Failed to install with Poetry: {stderr}")
    else:
        print_warning("Poetry not found, skipping dependency installation")
    
    # Create initial migration
    print_step(6, 8, "Creating initial migration...")
    code, _, stderr = run_command("python3 manage.py makemigrations", capture_output=True)
    if code == 0:
        print_success("Initial migration created")
    else:
        print_warning(f"Failed to create migration: {stderr}")
    
    # Run migrations
    print_step(7, 8, "Running migrations...")
    code, _, stderr = run_command("python3 manage.py migrate", capture_output=True)
    if code == 0:
        print_success("Migrations applied")
    else:
        print_warning(f"Failed to run migrations: {stderr}")
    
    # Final setup
    print_step(8, 8, "Finalizing setup...")
    
    duration = time.time() - start_time
    
    # Show success message
    console.print(Panel(
        f"[bold green]Project '{project_name}' created successfully![/bold green]\n\n"
        f"[bold]Next steps:[/bold]\n"
        f"  cd {project_name}\n"
        f"  corex runserver\n\n"
        f"  [bold]Or with Docker:[/bold]\n"
        f"  corex runserver --docker\n\n"
        f"[dim]Project created in {format_duration(duration)}[/dim]",
        title="🎉 Success!",
        border_style="green"
    ))
    
    # Show project structure
    if ctx.obj.get("verbose"):
        console.print("\n[bold]Project structure:[/bold]")
        from .utils import create_file_tree
        tree = create_file_tree(project_path, max_depth=2)
        console.print(tree)


def app_command(
    ctx: click.Context,
    app_name: str,
    app_type: Optional[str],
    auth: Optional[str],
    ui: Optional[str],
    seed: bool,
    api: bool,
) -> None:
    """Generate a new Django app with CoreX"""
    start_time = time.time()
    
    # Check if we're in a Django project
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        print_info("Run this command from your Django project root")
        return
    
    # Validate app name
    if not validate_project_name(app_name):
        print_error(f"Invalid app name: {app_name}")
        return
    
    # Check if app already exists
    app_path = project_root / app_name
    if app_path.exists():
        print_error(f"App '{app_name}' already exists")
        return
    
    # Get project configuration
    settings_path = project_root / "settings.py"
    if not settings_path.exists():
        # Try to find settings in project directory
        project_dirs = [d for d in project_root.iterdir() if d.is_dir() and (d / "settings.py").exists()]
        if project_dirs:
            settings_path = project_dirs[0] / "settings.py"
    
    if not settings_path.exists():
        print_error("Could not find Django settings file")
        return
    
    # Read project settings to determine auth and UI
    project_settings = {}
    try:
        with open(settings_path, 'r') as f:
            content = f.read()
            if 'rest_framework' in content:
                project_settings['api'] = True
            if 'tailwind' in content.lower():
                project_settings['ui'] = 'tailwind'
            elif 'bootstrap' in content.lower():
                project_settings['ui'] = 'bootstrap'
            else:
                project_settings['ui'] = 'none'
    except Exception:
        pass
    
    # Use project settings as defaults
    if auth is None:
        auth = "session"  # Default
    if ui is None:
        ui = project_settings.get('ui', 'none')
    
    print_step(1, 4, f"Generating app '{app_name}'...")
    success = generate_app(
        project_root,
        app_name,
        app_type,
        auth,
        ui,
        seed,
        api or project_settings.get('api', False)
    )
    
    if not success:
        print_error("Failed to generate app")
        return
    
    # Add app to INSTALLED_APPS
    print_step(2, 5, "Adding app to INSTALLED_APPS...")
    add_to_installed_apps(project_root, app_name)
    
    # Add app URLs to main project
    print_step(3, 5, "Adding app URLs to project...")
    add_to_project_urls(project_root, app_name)
    
    # Create migrations
    print_step(4, 5, "Creating migrations...")
    os.chdir(project_root)
    code, _, stderr = run_command(f"python3 manage.py makemigrations {app_name}", capture_output=True)
    if code == 0:
        print_success("Migrations created")
    else:
        print_warning(f"Failed to create migrations: {stderr}")
    
    # Run migrations
    print_step(5, 5, "Running migrations...")
    code, _, stderr = run_command(f"python3 manage.py migrate", capture_output=True)
    if code == 0:
        print_success("Migrations applied")
    else:
        print_warning(f"Failed to run migrations: {stderr}")
    
    duration = time.time() - start_time
    
    console.print(Panel(
        f"[bold green]App '{app_name}' generated successfully![/bold green]\n\n"
        f"[bold]What's next:[/bold]\n"
        f"  • Add URLs to your main urls.py\n"
        f"  • Customize models and views\n"
        f"  • Run: corex runserver\n\n"
        f"[dim]App generated in {format_duration(duration)}[/dim]",
        title="🎉 Success!",
        border_style="green"
    ))


def scaffold_command(
    ctx: click.Context,
    feature: str,
    app: Optional[str],
    model: Optional[str],
    fields: Optional[str],
) -> None:
    """Scaffold new features for existing apps"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    if not app:
        print_error("Please specify the target app with --app")
        return
    
    app_path = project_root / app
    if not app_path.exists():
        print_error(f"App '{app}' does not exist")
        return
    
    print_step(1, 3, f"Scaffolding {feature} for app '{app}'...")
    success = generate_scaffold(project_root, app, feature, model, fields)
    
    if not success:
        print_error("Failed to scaffold feature")
        return
    
    # Create migrations
    print_step(2, 3, "Creating migrations...")
    os.chdir(project_root)
    code, _, stderr = run_command(f"python3 manage.py makemigrations {app}", capture_output=True)
    if code == 0:
        print_success("Migrations created")
    else:
        print_warning(f"Failed to create migrations: {stderr}")
    
    # Run migrations
    print_step(3, 3, "Running migrations...")
    code, _, stderr = run_command(f"python3 manage.py migrate", capture_output=True)
    if code == 0:
        print_success("Migrations applied")
    else:
        print_warning(f"Failed to run migrations: {stderr}")
    
    console.print(Panel(
        f"[bold green]Feature '{feature}' scaffolded successfully![/bold green]\n\n"
        f"[bold]What's next:[/bold]\n"
        f"  • Customize the generated code\n"
        f"  • Add to your URLs\n"
        f"  • Test the new functionality\n",
        title="🎉 Success!",
        border_style="green"
    ))


def runserver_command(ctx: click.Context, docker: bool, port: int, host: str) -> None:
    """Run Django development server"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    os.chdir(project_root)
    
    if docker:
        # Check if docker-compose.yml exists
        docker_compose_file = project_root / "docker-compose.yml"
        if docker_compose_file.exists():
            print_info("Starting with Docker...")
            print_info("Building and starting containers...")
            cmd = "docker-compose up --build"
            run_command(cmd)
        else:
            print_error("Docker configuration not found")
            print_info("Run 'corex new' with --docker flag to create Docker setup")
            print_info("Or create a docker-compose.yml file manually")
    else:
        # Check if port is available
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print_warning(f"Port {port} is already in use")
            port += 1
            print_info(f"Trying port {port} instead...")
        
        print_info(f"Starting Django development server on {host}:{port}...")
        print_info(f"Visit: http://{host}:{port}/")
        
        # Run migrations first
        print_info("Checking for pending migrations...")
        code, stdout, _ = run_command("python3 manage.py showmigrations --plan", capture_output=True)
        if code == 0 and "[ ]" in stdout:
            print_info("Applying pending migrations...")
            run_command("python3 manage.py migrate", capture_output=True)
        
        cmd = f"python3 manage.py runserver {host}:{port}"
        run_command(cmd)


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


def ci_command(ctx: click.Context, github: bool, gitlab: bool, docker: bool) -> None:
    """Initialize CI/CD pipeline"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    if not github and not gitlab:
        print_error("Please specify --github or --gitlab")
        return
    
    print_step(1, 2, "Generating CI/CD pipeline...")
    success = generate_ci_pipeline(project_root, github, gitlab, docker)
    
    if success:
        print_step(2, 2, "Pipeline configuration complete")
        print_success("CI/CD pipeline generated successfully!")
        
        if github:
            print_info("GitHub Actions workflow created at .github/workflows/ci.yml")
        if gitlab:
            print_info("GitLab CI configuration created at .gitlab-ci.yml")
    else:
        print_error("Failed to generate CI/CD pipeline")


def integrate_command(ctx: click.Context, service: str, config: Optional[str]) -> None:
    """Integrate external services"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    print_step(1, 2, f"Integrating {service}...")
    success = generate_integration(project_root, service, config)
    
    if success:
        print_step(2, 2, "Integration complete")
        print_success(f"{service.title()} integration completed!")
        print_info(f"Check the generated configuration files")
    else:
        print_error(f"Failed to integrate {service}")


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
    if fix and issues:
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


def seed_command(ctx: click.Context, app: Optional[str], count: int) -> None:
    """Generate demo data for apps"""
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        return
    
    os.chdir(project_root)
    
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


def add_to_installed_apps(project_root: Path, app_name: str) -> None:
    """Add app to INSTALLED_APPS in settings"""
    # Find settings file
    settings_files = list(project_root.glob("**/settings.py"))
    if not settings_files:
        print_warning("Could not find settings.py")
        return
    
    settings_file = settings_files[0]
    
    try:
        content = settings_file.read_text()
        
        # Check if app is already in INSTALLED_APPS
        if f"'{app_name}'" in content or f'"{app_name}"' in content:
            print_info(f"App '{app_name}' already in INSTALLED_APPS")
            return
        
        # Find LOCAL_APPS first (CoreX pattern)
        lines = content.split('\n')
        in_local_apps = False
        added = False
        
        for i, line in enumerate(lines):
            if 'LOCAL_APPS' in line and '=' in line and '[' in line:
                in_local_apps = True
                continue
            
            if in_local_apps:
                if line.strip().startswith(']'):
                    # End of LOCAL_APPS, add before closing bracket
                    lines.insert(i, f"    '{app_name}',")
                    added = True
                    break
                elif line.strip().endswith(',') or '# Add' in line:
                    # Continue looking for the end
                    continue
        
        # If LOCAL_APPS pattern not found, try standard INSTALLED_APPS
        if not added:
            in_installed_apps = False
            for i, line in enumerate(lines):
                if 'INSTALLED_APPS' in line and '=' in line and '[' in line:
                    in_installed_apps = True
                    continue
                
                if in_installed_apps:
                    if line.strip().startswith(']'):
                        # End of INSTALLED_APPS, add before closing bracket
                        lines.insert(i, f"    '{app_name}',")
                        added = True
                        break
                    elif line.strip().endswith(','):
                        # Continue looking for the end
                        continue
        
        if added:
            settings_file.write_text('\n'.join(lines))
            print_success(f"Added '{app_name}' to INSTALLED_APPS")
        else:
            print_warning("Could not automatically add to INSTALLED_APPS")
            print_info(f"Please add '{app_name}' to INSTALLED_APPS manually")
    
    except Exception as e:
        print_warning(f"Could not update settings: {e}")
        print_info(f"Please add '{app_name}' to INSTALLED_APPS manually")


def add_to_project_urls(project_root: Path, app_name: str) -> None:
    """Add app URLs to main project urls.py"""
    # Find main project urls.py
    project_name = project_root.name
    urls_file = project_root / project_name / "urls.py"
    
    if not urls_file.exists():
        print_warning("Could not find main urls.py")
        return
    
    try:
        content = urls_file.read_text()
        
        # Check if app URLs are already included
        if f"include('{app_name}.urls')" in content:
            print_info(f"App '{app_name}' URLs already included")
            return
        
        # Find urlpatterns and add the app URL
        lines = content.split('\n')
        in_urlpatterns = False
        added = False
        
        for i, line in enumerate(lines):
            if 'urlpatterns' in line and '=' in line and '[' in line:
                in_urlpatterns = True
                continue
            
            if in_urlpatterns:
                if line.strip().startswith(']'):
                    # End of urlpatterns, add before closing bracket
                    lines.insert(i, f"    path('', include('{app_name}.urls')),  # {app_name.title()} as homepage")
                    added = True
                    break
                elif "path('admin/" in line:
                    # Add after admin path
                    lines.insert(i + 1, f"    path('', include('{app_name}.urls')),  # {app_name.title()} as homepage")
                    added = True
                    break
        
        if added:
            urls_file.write_text('\n'.join(lines))
            print_success(f"Added '{app_name}' URLs to main project")
        else:
            print_warning("Could not automatically add URLs to main project")
            print_info(f"Please add path('', include('{app_name}.urls')) to urlpatterns manually")
    
    except Exception as e:
        print_warning(f"Could not update urls.py: {e}")
        print_info(f"Please add path('', include('{app_name}.urls')) to urlpatterns manually")


def deploy_command(
    ctx: click.Context,
    platform: str,
    env_file: str,
    auto_db: bool,
    domain: Optional[str],
    region: Optional[str],
    force: bool,
) -> None:
    """Deploy Django project to cloud platforms"""
    start_time = time.time()
    
    # Check if we're in a Django project
    project_root = get_project_root()
    if not project_root:
        print_error("Not in a Django project directory")
        print_info("Run this command from your Django project root")
        return
    
    print_step(1, 8, f"Preparing deployment to {platform.title()}...")
    
    # Check environment file
    env_path = project_root / env_file
    if not env_path.exists() and not force:
        print_error(f"Environment file '{env_file}' not found")
        print_info("Create a .env file or use --env-file to specify a different file")
        return
    
    # Check project health
    print_step(2, 8, "Running project health check...")
    deps = check_dependencies()
    
    if not deps["git"] and not force:
        print_error("Git is required for deployment")
        print_info("Install Git or use --force to skip this check")
        return
    
    # Ensure git repository
    print_step(3, 8, "Checking git repository...")
    if not ensure_git_repo(project_root):
        print_warning("Could not initialize git repository")
    
    # Generate deployment configuration
    print_step(4, 8, f"Generating {platform} configuration...")
    success = generate_deployment(
        project_root, 
        platform, 
        env_file, 
        auto_db, 
        domain, 
        region
    )
    
    if not success:
        print_error("Failed to generate deployment configuration")
        return
    
    # Read environment variables
    print_step(5, 8, "Processing environment variables...")
    env_vars = {}
    if env_path.exists():
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
            print_success(f"Loaded {len(env_vars)} environment variables")
        except Exception as e:
            print_warning(f"Could not read environment file: {e}")
    
    # Platform-specific deployment steps
    print_step(6, 8, f"Executing {platform} deployment...")
    
    if platform == "vercel":
        deploy_to_vercel(project_root, env_vars, domain, region)
    elif platform == "railway":
        deploy_to_railway(project_root, env_vars, auto_db, domain, region)
    elif platform == "render":
        deploy_to_render(project_root, env_vars, auto_db, domain, region)
    elif platform == "heroku":
        deploy_to_heroku(project_root, env_vars, auto_db, domain, region)
    
    print_step(7, 8, "Finalizing deployment...")
    
    # Show deployment summary
    print_step(8, 8, "Deployment complete!")
    
    duration = time.time() - start_time
    
    console.print(Panel(
        f"[bold green]Deployment to {platform.title()} completed successfully![/bold green]\n\n"
        f"[bold]Platform:[/bold] {platform.title()}\n"
        f"[bold]Region:[/bold] {region or 'Default'}\n"
        f"[bold]Domain:[/bold] {domain or 'Auto-generated'}\n"
        f"[bold]Database:[/bold] {'Auto-provisioned' if auto_db else 'Manual setup required'}\n\n"
        f"[bold]Next steps:[/bold]\n"
        f"  • Monitor deployment logs\n"
        f"  • Configure custom domain (if needed)\n"
        f"  • Set up monitoring and alerts\n\n"
        f"[dim]Deployment completed in {format_duration(duration)}[/dim]",
        title="🚀 Deployment Success!",
        border_style="green"
    ))


def deploy_to_vercel(project_root: Path, env_vars: Dict[str, str], domain: Optional[str], region: Optional[str]) -> None:
    """Deploy to Vercel"""
    print_info("Setting up Vercel deployment...")
    
    # Check if Vercel CLI is installed
    code, _, _ = run_command("vercel --version", capture_output=True)
    if code != 0:
        print_warning("Vercel CLI not found")
        print_info("Install with: npm i -g vercel")
        print_info("Then run: vercel login")
        return
    
    # Deploy to Vercel
    os.chdir(project_root)
    
    print_info("Deploying to Vercel...")
    deploy_cmd = "vercel --prod"
    if domain:
        deploy_cmd += f" --name {domain}"
    
    code, stdout, stderr = run_command(deploy_cmd)
    if code == 0:
        print_success("Vercel deployment successful!")
        # Extract URL from output
        lines = stdout.split('\n')
        for line in lines:
            if 'https://' in line and 'vercel.app' in line:
                print_success(f"Your app is live at: {line.strip()}")
                break
    else:
        print_error(f"Vercel deployment failed: {stderr}")


def deploy_to_railway(project_root: Path, env_vars: Dict[str, str], auto_db: bool, domain: Optional[str], region: Optional[str]) -> None:
    """Deploy to Railway"""
    print_info("Setting up Railway deployment...")
    
    # Check if Railway CLI is installed
    code, _, _ = run_command("railway --version", capture_output=True)
    if code != 0:
        print_warning("Railway CLI not found")
        print_info("Install with: npm install -g @railway/cli")
        print_info("Then run: railway login")
        return
    
    # Initialize Railway project
    os.chdir(project_root)
    
    print_info("Initializing Railway project...")
    code, _, _ = run_command("railway init", capture_output=True)
    
    # Add PostgreSQL if requested
    if auto_db:
        print_info("Adding PostgreSQL database...")
        code, _, stderr = run_command("railway add postgresql", capture_output=True)
        if code == 0:
            print_success("PostgreSQL database added")
        else:
            print_warning(f"Could not add database: {stderr}")
    
    # Set environment variables
    print_info("Setting environment variables...")
    for key, value in env_vars.items():
        if key not in ['SECRET_KEY', 'DEBUG']:  # Skip sensitive vars
            run_command(f"railway variables set {key}={value}", capture_output=True)
    
    # Deploy
    print_info("Deploying to Railway...")
    code, stdout, stderr = run_command("railway up")
    if code == 0:
        print_success("Railway deployment successful!")
        # Get the URL
        code, url_output, _ = run_command("railway domain", capture_output=True)
        if code == 0 and url_output.strip():
            print_success(f"Your app is live at: https://{url_output.strip()}")
    else:
        print_error(f"Railway deployment failed: {stderr}")


def deploy_to_render(project_root: Path, env_vars: Dict[str, str], auto_db: bool, domain: Optional[str], region: Optional[str]) -> None:
    """Deploy to Render"""
    print_info("Setting up Render deployment...")
    print_info("Render deployment requires manual setup through the web interface")
    
    # Show instructions
    console.print(Panel(
        "[bold]Render Deployment Instructions:[/bold]\n\n"
        "1. Push your code to GitHub/GitLab\n"
        "2. Go to https://dashboard.render.com\n"
        "3. Click 'New +' and select 'Web Service'\n"
        "4. Connect your repository\n"
        "5. Configure the following settings:\n\n"
        "   [bold]Build Command:[/bold] pip install -r requirements.txt\n"
        "   [bold]Start Command:[/bold] gunicorn myproject.wsgi:application\n"
        "   [bold]Environment:[/bold] Python 3\n\n"
        "6. Add environment variables from your .env file\n"
        f"7. {'Add PostgreSQL database from the dashboard' if auto_db else 'Configure your database connection'}\n"
        "8. Deploy!\n",
        title="📋 Manual Setup Required",
        border_style="blue"
    ))


def deploy_to_heroku(project_root: Path, env_vars: Dict[str, str], auto_db: bool, domain: Optional[str], region: Optional[str]) -> None:
    """Deploy to Heroku"""
    print_info("Setting up Heroku deployment...")
    
    # Check if Heroku CLI is installed
    code, _, _ = run_command("heroku --version", capture_output=True)
    if code != 0:
        print_warning("Heroku CLI not found")
        print_info("Install from: https://devcenter.heroku.com/articles/heroku-cli")
        print_info("Then run: heroku login")
        return
    
    # Create Heroku app
    os.chdir(project_root)
    app_name = domain or project_root.name
    
    print_info(f"Creating Heroku app '{app_name}'...")
    create_cmd = f"heroku create {app_name}"
    if region:
        create_cmd += f" --region {region}"
    
    code, stdout, stderr = run_command(create_cmd, capture_output=True)
    if code != 0 and "already exists" not in stderr:
        print_warning(f"Could not create app: {stderr}")
        app_name = f"{app_name}-{int(time.time())}"
        print_info(f"Trying with name: {app_name}")
        code, _, _ = run_command(f"heroku create {app_name}", capture_output=True)
    
    # Add PostgreSQL if requested
    if auto_db:
        print_info("Adding PostgreSQL database...")
        code, _, stderr = run_command("heroku addons:create heroku-postgresql:hobby-dev", capture_output=True)
        if code == 0:
            print_success("PostgreSQL database added")
        else:
            print_warning(f"Could not add database: {stderr}")
    
    # Set environment variables
    print_info("Setting environment variables...")
    for key, value in env_vars.items():
        if key not in ['DATABASE_URL']:  # Skip Heroku-managed vars
            run_command(f"heroku config:set {key}={value}", capture_output=True)
    
    # Deploy
    print_info("Deploying to Heroku...")
    code, stdout, stderr = run_command("git push heroku main")
    if code == 0:
        print_success("Heroku deployment successful!")
        # Get the URL
        code, url_output, _ = run_command("heroku info -s | grep web_url", capture_output=True)
        if code == 0:
            url = url_output.split('=')[1].strip() if '=' in url_output else ''
            if url:
                print_success(f"Your app is live at: {url}")
    else:
        print_error(f"Heroku deployment failed: {stderr}")
