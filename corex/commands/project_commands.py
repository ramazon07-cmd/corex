"""
CoreX Project Commands
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

import click
from rich.console import Console
from rich.panel import Panel

from .. import generators
from ..utils import (
    check_dependencies,
    create_gitignore,
    ensure_git_repo,
    format_duration,
    print_error,
    print_info,
    print_step,
    print_success,
    print_warning,
    run_command,
    validate_project_name,
    create_file_tree,
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
    success = generators.generate_project(project_path, project_name, auth, ui, database, docker, api)
    
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
        tree = create_file_tree(project_path, max_depth=2)
        console.print(tree)