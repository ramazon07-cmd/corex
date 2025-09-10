"""
CoreX CLI - Main entry point for all commands
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .commands import (
    app_command,
    ci_command,
    deploy_command,
    doctor_command,
    integrate_command,
    new_command,
    runserver_command,
    scaffold_command,
    seed_command,
    test_command,
)
from .utils import get_project_root

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="CoreX")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """
    CoreX - A comprehensive Django scaffolding framework
    
    Create production-ready Django apps with a single command.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    
    if verbose:
        console.print("[bold blue]CoreX[/bold blue] - Django Scaffolding Framework")


@main.command()
@click.argument("project_name")
@click.option("--auth", type=click.Choice(["jwt", "session", "allauth"]), default="session", help="Authentication method")
@click.option("--ui", type=click.Choice(["tailwind", "bootstrap", "none"]), default="tailwind", help="UI framework")
@click.option("--database", type=click.Choice(["postgres", "mysql", "sqlite"]), default="sqlite", help="Database backend")
@click.option("--docker", is_flag=True, help="Include Docker configuration")
@click.option("--api", is_flag=True, help="Include DRF API setup")
@click.pass_context
def new(ctx: click.Context, project_name: str, auth: str, ui: str, database: str, docker: bool, api: bool) -> None:
    """Create a new Django project with CoreX"""
    new_command(ctx, project_name, auth, ui, database, docker, api)


@main.command()
@click.argument("app_name")
@click.option("--type", type=click.Choice(["blog", "portfolio", "forum", "wiki", "elearn", "social", "crm", "shop"]), help="App type")
@click.option("--auth", type=click.Choice(["jwt", "session", "allauth"]), help="Authentication method")
@click.option("--ui", type=click.Choice(["tailwind", "bootstrap", "none"]), help="UI framework")
@click.option("--seed", is_flag=True, help="Generate demo data")
@click.option("--api", is_flag=True, help="Include API endpoints")
@click.pass_context
def app(ctx: click.Context, app_name: str, type: Optional[str], auth: Optional[str], ui: Optional[str], seed: bool, api: bool) -> None:
    """Generate a new Django app with CoreX"""
    app_command(ctx, app_name, type, auth, ui, seed, api)


@main.command()
@click.argument("feature")
@click.option("--app", help="Target app name")
@click.option("--model", help="Model name")
@click.option("--fields", help="Model fields (format: name:type:options)")
@click.pass_context
def scaffold(ctx: click.Context, feature: str, app: Optional[str], model: Optional[str], fields: Optional[str]) -> None:
    """Scaffold new features for existing apps"""
    scaffold_command(ctx, feature, app, model, fields)


@main.command()
@click.option("--docker", is_flag=True, help="Run with Docker")
@click.option("--port", default=8000, help="Port to run server on")
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.pass_context
def runserver(ctx: click.Context, docker: bool, port: int, host: str) -> None:
    """Run Django development server"""
    runserver_command(ctx, docker, port, host)


@main.command()
@click.option("--app", help="Run migrations for specific app")
@click.option("--fake", is_flag=True, help="Mark migrations as applied without running them")
@click.pass_context
def migrate(ctx: click.Context, app: Optional[str], fake: bool) -> None:
    """Run Django migrations"""
    project_root = get_project_root()
    if not project_root:
        console.print("[red]Error:[/red] Not in a Django project directory")
        sys.exit(1)
    
    os.chdir(project_root)
    cmd = f"python3 manage.py migrate"
    if app:
        cmd += f" {app}"
    if fake:
        cmd += " --fake"
    
    console.print(f"[green]Running:[/green] {cmd}")
    os.system(cmd)


@main.command()
@click.option("--username", help="Admin username")
@click.option("--email", help="Admin email")
@click.option("--noinput", is_flag=True, help="Don't prompt for input")
@click.pass_context
def createsuperuser(ctx: click.Context, username: Optional[str], email: Optional[str], noinput: bool) -> None:
    """Create Django superuser"""
    project_root = get_project_root()
    if not project_root:
        console.print("[red]Error:[/red] Not in a Django project directory")
        sys.exit(1)
    
    os.chdir(project_root)
    cmd = "python3 manage.py createsuperuser"
    if username:
        cmd += f" --username {username}"
    if email:
        cmd += f" --email {email}"
    if noinput:
        cmd += " --noinput"
    
    console.print(f"[green]Running:[/green] {cmd}")
    os.system(cmd)


@main.command()
@click.argument("app_name", required=False)
@click.option("--coverage", is_flag=True, help="Run tests with coverage")
@click.option("--parallel", is_flag=True, help="Run tests in parallel")
@click.pass_context
def test(ctx: click.Context, app_name: Optional[str], coverage: bool, parallel: bool) -> None:
    """Run Django tests"""
    test_command(ctx, app_name, coverage, parallel)


@main.command()
@click.option("--github", is_flag=True, help="Generate GitHub Actions workflow")
@click.option("--gitlab", is_flag=True, help="Generate GitLab CI configuration")
@click.option("--docker", is_flag=True, help="Include Docker in CI/CD")
@click.pass_context
def ci(ctx: click.Context, github: bool, gitlab: bool, docker: bool) -> None:
    """Initialize CI/CD pipeline"""
    ci_command(ctx, github, gitlab, docker)


@main.command()
@click.argument("service", type=click.Choice(["stripe", "s3", "elasticsearch", "redis", "celery", "email"]))
@click.option("--config", help="Configuration file path")
@click.pass_context
def integrate(ctx: click.Context, service: str, config: Optional[str]) -> None:
    """Integrate external services"""
    integrate_command(ctx, service, config)


@main.command()
@click.option("--fix", is_flag=True, help="Attempt to fix issues")
@click.pass_context
def doctor(ctx: click.Context, fix: bool) -> None:
    """Check environment health and diagnose issues"""
    doctor_command(ctx, fix)


@main.command()
@click.option("--app", help="Generate seeds for specific app")
@click.option("--count", default=10, help="Number of records to generate")
@click.pass_context
def seed(ctx: click.Context, app: Optional[str], count: int) -> None:
    """Generate demo data for apps"""
    seed_command(ctx, app, count)


@main.command()
@click.option("--platform", type=click.Choice(["vercel", "railway", "render", "heroku"]), required=True, help="Deployment platform")
@click.option("--env-file", default=".env", help="Environment file to use")
@click.option("--auto-db", is_flag=True, help="Automatically provision database")
@click.option("--domain", help="Custom domain name")
@click.option("--region", help="Deployment region")
@click.option("--force", is_flag=True, help="Force deployment even if checks fail")
@click.pass_context
def deploy(ctx: click.Context, platform: str, env_file: str, auto_db: bool, domain: Optional[str], region: Optional[str], force: bool) -> None:
    """Deploy Django project to cloud platforms"""
    deploy_command(ctx, platform, env_file, auto_db, domain, region, force)


if __name__ == "__main__":
    main()
