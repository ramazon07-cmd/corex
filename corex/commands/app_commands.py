"""
CoreX App Commands
"""

import os
import time
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel

from .. import generators
from ..utils import (
    get_project_root,
    print_error,
    print_info,
    print_step,
    print_success,
    print_warning,
    run_command,
    validate_project_name,
    format_duration,
)

console = Console()


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
    success = generators.generate_app(
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
    success = generators.generate_scaffold(project_root, app, feature, model, fields)
    
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