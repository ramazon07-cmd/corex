"""
CoreX Deployment Commands
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
    check_dependencies,
    format_duration,
    ensure_git_repo,
)

console = Console()


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
    success = generators.generate_ci_pipeline(project_root, github, gitlab, docker)
    
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
    success = generators.generate_integration(project_root, service, config)
    
    if success:
        print_step(2, 2, "Integration complete")
        print_success(f"{service.title()} integration completed!")
        print_info(f"Check the generated configuration files")
    else:
        print_error(f"Failed to integrate {service}")


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
    success = generators.generate_deployment(
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