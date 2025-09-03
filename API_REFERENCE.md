# CoreX API Reference

**Complete programmatic interface documentation for CoreX Django scaffolding framework**

## Table of Contents

1. [CLI Interface](#cli-interface)
2. [Core Modules](#core-modules)
3. [Generator Functions](#generator-functions)
4. [Utility Functions](#utility-functions)
5. [Template System](#template-system)
6. [Configuration Schema](#configuration-schema)
7. [Extension Points](#extension-points)

---

## CLI Interface

### Main Command Group

**`corex.cli.main()`**

The main Click command group that serves as the entry point for all CoreX commands.

```python
@click.group()
@click.version_option(version="1.0.0", prog_name="CoreX")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None
```

### Project Management Commands

#### `new` Command

Create a new Django project with comprehensive configuration.

```python
@main.command()
@click.argument("project_name")
@click.option("--auth", type=click.Choice(["jwt", "session", "allauth"]), default="session")
@click.option("--ui", type=click.Choice(["tailwind", "bootstrap", "none"]), default="tailwind")
@click.option("--database", type=click.Choice(["postgres", "mysql", "sqlite"]), default="sqlite")
@click.option("--docker", is_flag=True)
@click.option("--api", is_flag=True)
@click.pass_context
def new(ctx, project_name, auth, ui, database, docker, api) -> None
```

**Parameters:**
- `project_name` (str): Valid Python identifier for the project
- `auth` (str): Authentication method - "jwt", "session", or "allauth"
- `ui` (str): UI framework - "tailwind", "bootstrap", or "none"
- `database` (str): Database backend - "postgres", "mysql", or "sqlite"
- `docker` (bool): Include Docker configuration files
- `api` (bool): Include Django REST Framework setup

**Returns:** None (exits with code 0 on success, 1 on failure)

#### `app` Command

Generate a new Django app with specialized templates.

```python
@main.command()
@click.argument("app_name")
@click.option("--type", type=click.Choice(["blog", "portfolio", "forum", "wiki", "elearn", "social", "crm", "shop"]))
@click.option("--auth", type=click.Choice(["jwt", "session", "allauth"]))
@click.option("--ui", type=click.Choice(["tailwind", "bootstrap", "none"]))
@click.option("--seed", is_flag=True)
@click.option("--api", is_flag=True)
@click.pass_context
def app(ctx, app_name, type, auth, ui, seed, api) -> None
```

#### `runserver` Command

Start the Django development server with optional Docker support.

```python
@main.command()
@click.option("--docker", is_flag=True)
@click.option("--port", default=8000)
@click.option("--host", default="127.0.0.1")
@click.pass_context
def runserver(ctx, docker, port, host) -> None
```

---

## Core Modules

### `corex.commands`

Contains the implementation logic for all CLI commands.

#### `new_command()`

```python
def new_command(
    ctx: click.Context,
    project_name: str,
    auth: str,
    ui: str,
    database: str,
    docker: bool,
    api: bool,
) -> None
```

**Implementation Steps:**
1. Validates project name using `validate_project_name()`
2. Checks if directory already exists
3. Verifies system dependencies with `check_dependencies()`
4. Generates project structure using `generate_project()`
5. Initializes Git repository with `ensure_git_repo()`
6. Creates .gitignore file with `create_gitignore()`
7. Installs dependencies (Poetry preferred)
8. Creates and applies initial migrations

#### `app_command()`

```python
def app_command(
    ctx: click.Context,
    app_name: str,
    app_type: Optional[str],
    auth: Optional[str],
    ui: Optional[str],
    seed: bool,
    api: bool,
) -> None
```

**Implementation Steps:**
1. Validates Django project context
2. Checks app name validity
3. Reads project configuration from settings.py
4. Generates app using `generate_app()`
5. Adds app to INSTALLED_APPS
6. Creates and runs migrations

#### `test_command()`

```python
def test_command(
    ctx: click.Context,
    app_name: Optional[str],
    coverage: bool,
    parallel: bool,
) -> None
```

**Features:**
- Runs Django test suite
- Optional coverage reporting with HTML output
- Parallel test execution support
- App-specific testing

---

## Generator Functions

### `corex.generators`

Core code generation functionality using Jinja2 templates.

#### `generate_project()`

```python
def generate_project(
    project_path: Path,
    project_name: str,
    auth: str,
    ui: str,
    database: str,
    docker: bool,
    api: bool,
) -> bool
```

**Generates:**
- Django project structure
- Configuration files (settings.py, urls.py, etc.)
- Static and media directories
- Templates directory with base.html
- Docker configuration (if enabled)
- UI framework files (if specified)
- API configuration (if enabled)

**Template Context:**
```python
context = {
    "project_name": str,
    "auth": str,
    "ui": str,
    "database": str,
    "docker": bool,
    "api": bool,
    "python_version": str,
}
```

#### `generate_app()`

```python
def generate_app(
    project_root: Path,
    app_name: str,
    app_type: Optional[str],
    auth: Optional[str],
    ui: Optional[str],
    seed: bool,
    api: bool
) -> bool
```

**App Type Templates:**

| Type | Models | Views | Templates | API | Tests |
|------|--------|-------|-----------|-----|-------|
| `blog` | Post, Comment, Category, Tag | ListView, DetailView, CreateView | post_list.html, post_detail.html | PostViewSet, CommentViewSet | ✅ |
| `shop` | Product, Order, Cart, Category | ProductView, CartView, CheckoutView | product_list.html, cart.html | ProductAPI, OrderAPI | ✅ |
| `wiki` | Page, Revision, Category | PageView, EditView, HistoryView | page_view.html, page_edit.html | PageAPI, RevisionAPI | ✅ |
| `crm` | Contact, Deal, Task, Company | ContactView, DealView, TaskView | contact_list.html, deal_pipeline.html | ContactAPI, DealAPI | ✅ |

#### `generate_scaffold()`

```python
def generate_scaffold(
    project_root: Path,
    app: str,
    feature: str,
    model: Optional[str],
    fields: Optional[str]
) -> bool
```

**Supported Features:**
- `model`: Generate Django models with fields
- `view`: Generate class-based views
- `api`: Generate DRF serializers and viewsets
- `form`: Generate Django forms
- `admin`: Generate admin interface

---

## Utility Functions

### `corex.utils`

Helper functions for file operations, validation, and system interaction.

#### Core Utilities

```python
def get_project_root() -> Optional[Path]
```
Detects Django project root by looking for manage.py.

```python
def validate_project_name(name: str) -> bool
```
Validates project name as a Python identifier.

```python
def check_dependencies() -> Dict[str, bool]
```
Checks for Poetry, Docker, Git, and Python availability.

```python
def run_command(cmd: str, cwd: Optional[Path] = None, capture_output: bool = False) -> Tuple[int, str, str]
```
Executes shell commands with error handling.

#### File Operations

```python
def create_directory(path: Path, parents: bool = True) -> None
```
Creates directories with parent directory support.

```python
def copy_template_file(template_path: Path, destination_path: Path, context: Dict = None) -> None
```
Copies template files with Jinja2 context substitution.

```python
def get_template_path(template_name: str) -> Path
```
Resolves template file paths within the CoreX package.

#### Display Functions

```python
def print_success(message: str) -> None
def print_error(message: str) -> None
def print_warning(message: str) -> None
def print_info(message: str) -> None
def print_step(step: int, total: int, message: str) -> None
```

Rich console output functions with consistent styling.

---

## Template System

### Template Directory Structure

```
corex/templates/
├── projects/
│   ├── manage.py.j2
│   ├── settings.py.j2
│   ├── urls.py.j2
│   ├── wsgi.py.j2
│   ├── asgi.py.j2
│   ├── base.html.j2
│   ├── pyproject.toml.j2
│   ├── README.md.j2
│   ├── env.j2
│   ├── requirements.txt.j2
│   ├── Dockerfile.j2
│   ├── docker-compose.yml.j2
│   └── ui/
│       ├── tailwind/
│       └── bootstrap/
├── apps/
│   ├── types/
│   │   ├── blog/
│   │   ├── shop/
│   │   ├── wiki/
│   │   └── crm/
│   ├── models.py.j2
│   ├── views.py.j2
│   ├── urls.py.j2
│   ├── admin.py.j2
│   ├── forms.py.j2
│   ├── serializers.py.j2
│   └── tests/
└── ci/
    ├── github/
    └── gitlab/
```

### Template Variables

#### Project Templates

```python
{
    "project_name": "myproject",
    "auth": "jwt|session|allauth",
    "ui": "tailwind|bootstrap|none",
    "database": "postgres|mysql|sqlite",
    "docker": True|False,
    "api": True|False,
    "python_version": "3.9"
}
```

#### App Templates

```python
{
    "app_name": "blog",
    "app_type": "blog|shop|wiki|crm|social|forum",
    "project_name": "myproject",
    "auth": "jwt|session|allauth",
    "ui": "tailwind|bootstrap|none",
    "seed": True|False,
    "api": True|False,
    "models": [
        {
            "name": "Post",
            "fields": [
                {"name": "title", "type": "CharField", "options": "max_length=200"},
                {"name": "content", "type": "TextField"},
                {"name": "created_at", "type": "DateTimeField", "options": "auto_now_add=True"}
            ]
        }
    ]
}
```

---

## Configuration Schema

### Project Configuration

```python
class ProjectConfig:
    name: str
    auth: Literal["jwt", "session", "allauth"]
    ui: Literal["tailwind", "bootstrap", "none"]
    database: Literal["postgres", "mysql", "sqlite"]
    docker: bool
    api: bool
    python_version: str = "3.9"
```

### App Configuration

```python
class AppConfig:
    name: str
    type: Optional[Literal["blog", "shop", "wiki", "crm", "social", "forum", "portfolio", "elearn"]]
    auth: Optional[str]
    ui: Optional[str]
    seed: bool = False
    api: bool = False
```

### Database Configuration

```python
DATABASE_CONFIGS = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3"
    },
    "postgres": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "{{ project_name }}",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432"
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ project_name }}",
        "USER": "root",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "3306"
    }
}
```

---

## Extension Points

### Custom Templates

Create custom app templates:

```python
def register_custom_template(template_name: str, template_path: Path) -> None:
    """Register a custom app template"""
    pass

def get_available_templates() -> List[str]:
    """Get list of available app templates"""
    return ["blog", "shop", "wiki", "crm", "social", "forum", "portfolio", "elearn"]
```

### Custom Generators

Extend generation functionality:

```python
def custom_generator(
    project_root: Path,
    config: Dict[str, Any]
) -> bool:
    """Custom code generator"""
    pass
```

### Hooks

Pre and post-generation hooks:

```python
def before_project_generation(config: ProjectConfig) -> None:
    """Called before project generation"""
    pass

def after_project_generation(project_path: Path, config: ProjectConfig) -> None:
    """Called after project generation"""
    pass

def before_app_generation(config: AppConfig) -> None:
    """Called before app generation"""
    pass

def after_app_generation(app_path: Path, config: AppConfig) -> None:
    """Called after app generation"""
    pass
```

---

## Error Handling

### Exception Types

```python
class CoreXError(Exception):
    """Base CoreX exception"""
    pass

class ProjectExistsError(CoreXError):
    """Project directory already exists"""
    pass

class InvalidProjectNameError(CoreXError):
    """Invalid project name provided"""
    pass

class TemplateNotFoundError(CoreXError):
    """Template file not found"""
    pass

class GenerationError(CoreXError):
    """Error during code generation"""
    pass
```

### Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Project not found |
| 4 | Template error |
| 5 | System dependency missing |

---

## Testing Interface

### Test Utilities

```python
def create_test_project(
    temp_dir: Path,
    project_name: str = "test_project",
    **kwargs
) -> Path:
    """Create a test project for testing"""
    pass

def assert_file_exists(project_path: Path, file_path: str) -> None:
    """Assert that a file exists in the project"""
    pass

def assert_file_contains(project_path: Path, file_path: str, content: str) -> None:
    """Assert that a file contains specific content"""
    pass
```

---

This API reference provides complete programmatic access to CoreX functionality for advanced users and contributors.