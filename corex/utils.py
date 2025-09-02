"""
CoreX utilities and helper functions
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()


def get_project_root() -> Optional[Path]:
    """Detect if we're in a Django project and return the root path"""
    current = Path.cwd()
    
    # Look for manage.py in current directory or parents
    while current != current.parent:
        if (current / "manage.py").exists():
            return current
        current = current.parent
    
    return None


def is_django_project(path: Path) -> bool:
    """Check if a directory contains a Django project"""
    return (path / "manage.py").exists() and (path / "settings.py").exists()


def run_command(cmd: str, cwd: Optional[Path] = None, capture_output: bool = False) -> Tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=False
        )
        return result.returncode, result.stdout or "", result.stderr or ""
    except Exception as e:
        return 1, "", str(e)


def create_directory(path: Path, parents: bool = True) -> None:
    """Create a directory if it doesn't exist"""
    path.mkdir(parents=parents, exist_ok=True)


def copy_template_file(template_path: Path, destination_path: Path, context: Dict = None) -> None:
    """Copy a template file to destination with optional context substitution"""
    if context is None:
        context = {}
    
    # Create destination directory if it doesn't exist
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read template content
    content = template_path.read_text()
    
    # Apply context substitutions
    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))
    
    # Write to destination
    destination_path.write_text(content)


def get_template_path(template_name: str) -> Path:
    """Get the path to a template file"""
    corex_root = Path(__file__).parent
    return corex_root / "templates" / template_name


def validate_project_name(name: str) -> bool:
    """Validate project name (no spaces, valid Python identifier)"""
    if not name or " " in name:
        return False
    
    # Check if it's a valid Python identifier
    if not name[0].isalpha() and name[0] != "_":
        return False
    
    for char in name[1:]:
        if not char.isalnum() and char != "_":
            return False
    
    return True


def get_python_version() -> str:
    """Get current Python version"""
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed"""
    deps = {
        "poetry": False,
        "docker": False,
        "git": False,
        "python": True,  # We're running Python
    }
    
    # Check Poetry
    code, _, _ = run_command("poetry --version", capture_output=True)
    deps["poetry"] = code == 0
    
    # Check Docker
    code, _, _ = run_command("docker --version", capture_output=True)
    deps["docker"] = code == 0
    
    # Check Git
    code, _, _ = run_command("git --version", capture_output=True)
    deps["git"] = code == 0
    
    return deps


def print_success(message: str) -> None:
    """Print a success message"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print an error message"""
    console.print(f"[red]✗[/red] {message}")


def print_warning(message: str) -> None:
    """Print a warning message"""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Print an info message"""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_step(step: int, total: int, message: str) -> None:
    """Print a step message with progress"""
    console.print(f"[cyan][{step}/{total}][/cyan] {message}")


def show_progress_spinner(message: str):
    """Context manager for showing a progress spinner"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    )


def create_file_tree(path: Path, max_depth: int = 3) -> str:
    """Create a visual file tree representation"""
    tree = []
    
    def add_to_tree(current_path: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        
        items = sorted(current_path.iterdir(), key=lambda x: (x.is_file(), x.name))
        
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            current_prefix = "└── " if is_last else "├── "
            next_prefix = "    " if is_last else "│   "
            
            if item.is_dir():
                tree.append(f"{prefix}{current_prefix}[blue]{item.name}/[/blue]")
                add_to_tree(item, prefix + next_prefix, depth + 1)
            else:
                tree.append(f"{prefix}{current_prefix}{item.name}")
    
    add_to_tree(path, "", 0)
    return "\n".join(tree)


def get_app_templates() -> List[str]:
    """Get list of available app templates"""
    return [
        "blog",
        "portfolio", 
        "forum",
        "wiki",
        "elearn",
        "social",
        "crm",
        "shop"
    ]


def get_auth_options() -> List[str]:
    """Get list of available authentication options"""
    return ["jwt", "session", "allauth"]


def get_ui_options() -> List[str]:
    """Get list of available UI framework options"""
    return ["tailwind", "bootstrap", "none"]


def get_database_options() -> List[str]:
    """Get list of available database options"""
    return ["postgres", "mysql", "sqlite"]


def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    return filename


def get_relative_path(path: Path, base: Path) -> str:
    """Get relative path from base directory"""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def ensure_git_repo(path: Path) -> bool:
    """Ensure a directory is a git repository, initialize if needed"""
    git_dir = path / ".git"
    
    if git_dir.exists():
        return True
    
    # Initialize git repository
    code, _, _ = run_command("git init", cwd=path, capture_output=True)
    if code == 0:
        print_success("Initialized git repository")
        return True
    else:
        print_warning("Failed to initialize git repository")
        return False


def create_gitignore(path: Path) -> None:
    """Create a comprehensive .gitignore file for Django projects"""
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Docker
.dockerignore

# Redis
dump.rdb

# Elasticsearch
data/

# Logs
logs/
*.log

# Media files (if not using CDN)
media/

# Static files (if not using CDN)
staticfiles/

# Database
*.db
*.sqlite3

# Backup files
*.bak
*.backup

# Temporary files
*.tmp
*.temp
"""
    
    gitignore_path = path / ".gitignore"
    gitignore_path.write_text(gitignore_content)
    print_success("Created .gitignore file")
