# CoreX Usage Documentation

**Complete Guide to Using CoreX Django Scaffolding Framework**

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Core Commands](#core-commands)
4. [Project Management](#project-management)
5. [App Development](#app-development)
6. [Advanced Features](#advanced-features)
7. [Configuration Options](#configuration-options)
8. [Testing & Development](#testing--development)
9. [Deployment & CI/CD](#deployment--cicd)
10. [Troubleshooting](#troubleshooting)
11. [Examples & Workflows](#examples--workflows)

---

## Quick Start

Get started with CoreX in under 5 minutes:

```bash
# Install CoreX
pip install corex

# Create a new Django project
corex new myproject --auth=jwt --ui=tailwind --database=postgres --api

# Navigate to project
cd myproject

# Start development server
corex runserver

# Visit http://localhost:8000
```

---

## Installation

### Prerequisites

- Python 3.9+ 
- pip or Poetry
- Git (recommended)
- Docker (optional)

### Install CoreX

```bash
# Using pip
pip install corex

# Using Poetry
poetry add corex

# Verify installation
corex --version
```

### Check Environment

```bash
# Check system dependencies and health
corex doctor

# Auto-fix common issues
corex doctor --fix
```

---

## Core Commands

CoreX provides a comprehensive set of commands for Django development:

### Project Commands
- [`corex new`](#creating-projects) - Create new Django projects
- [`corex runserver`](#running-development-server) - Start development server
- [`corex migrate`](#database-management) - Run database migrations
- [`corex test`](#testing) - Run tests with coverage
- [`corex doctor`](#health-checks) - Check project health

### App Development Commands
- [`corex app`](#generating-apps) - Generate specialized Django apps
- [`corex scaffold`](#scaffolding-features) - Add features to existing apps
- [`corex seed`](#generating-demo-data) - Generate demo data

### DevOps Commands
- [`corex ci`](#cicd-setup) - Setup CI/CD pipelines
- [`corex integrate`](#service-integrations) - Integrate external services
- [`corex deploy`](#deployment) - Deploy to cloud platforms

---

## Project Management

### Creating Projects

Create a new Django project with comprehensive configuration:

```bash
corex new PROJECT_NAME [OPTIONS]
```

**Available Options:**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--auth` | `jwt`, `session`, `allauth` | `session` | Authentication method |
| `--ui` | `tailwind`, `bootstrap`, `none` | `tailwind` | UI framework |
| `--database` | `postgres`, `mysql`, `sqlite` | `sqlite` | Database backend |
| `--docker` | flag | disabled | Include Docker configuration |
| `--api` | flag | disabled | Include Django REST Framework |

**Examples:**

```bash
# Basic project with defaults
corex new myblog

# Full-featured project
corex new ecommerce --auth=jwt --ui=tailwind --database=postgres --docker --api

# API-only project
corex new api_service --auth=jwt --ui=none --database=postgres --api

# Social authentication project
corex new social_app --auth=allauth --ui=bootstrap --database=mysql
```

**Generated Project Structure:**

```
myproject/
├── myproject/          # Main project package
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL configuration
│   ├── wsgi.py         # WSGI application
│   └── asgi.py         # ASGI application
├── static/             # Static files
├── media/              # User uploads
├── templates/          # HTML templates
├── logs/               # Application logs
├── manage.py           # Django management script
├── pyproject.toml      # Poetry dependencies
├── requirements.txt    # Pip requirements
├── Dockerfile          # Docker image (if --docker)
├── docker-compose.yml  # Docker services (if --docker)
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

### Running Development Server

Start your Django development server:

```bash
# Basic usage
corex runserver

# Custom port and host
corex runserver --port=8001 --host=0.0.0.0

# Using Docker
corex runserver --docker
```

**Features:**
- Automatic migration checking
- Port conflict detection
- Hot reload support
- Docker integration

### Database Management

Manage your Django database:

```bash
# Run all pending migrations
corex migrate

# Run migrations for specific app
corex migrate --app=blog

# Mark migrations as applied without running
corex migrate --fake
```

### Creating Superuser

Create Django admin users:

```bash
# Interactive creation
corex createsuperuser

# Non-interactive with details
corex createsuperuser --username=admin --email=admin@example.com --noinput
```

---

## App Development

### Generating Apps

CoreX provides specialized app templates for rapid development:

```bash
corex app APP_NAME --type=TYPE [OPTIONS]
```

**Available App Types:**

| Type | Description | Models | Features |
|------|-------------|--------|----------|
| `blog` | Blog application | Post, Comment, Category, Tag | Rich editor, SEO, social sharing |
| `shop` | E-commerce | Product, Order, Cart, Category | Inventory, payments, checkout |
| `wiki` | Documentation/Wiki | Page, Revision, Category | Version control, Markdown, search |
| `crm` | Customer Relations | Contact, Deal, Task, Company | Pipeline, activity tracking |
| `social` | Social Network | Profile, Post, Follow, Like | Activity feeds, messaging |
| `forum` | Discussion Forum | Topic, Post, Category | Moderation, user reputation |
| `portfolio` | Portfolio Site | Project, Skill, Experience | Gallery, contact forms |
| `elearn` | E-learning | Course, Lesson, Enrollment | Progress tracking, quizzes |

**App Generation Options:**

| Option | Description |
|--------|-------------|
| `--seed` | Generate demo data |
| `--api` | Include API endpoints |
| `--auth` | Override project auth method |
| `--ui` | Override project UI framework |

**Examples:**

```bash
# Create a blog with demo data
corex app blog --type=blog --seed

# Create an e-commerce app with API
corex app store --type=shop --api

# Create a documentation wiki
corex app docs --type=wiki --ui=tailwind

# Create a CRM system
corex app sales --type=crm --auth=jwt
```

**Generated App Structure:**

```
blog/
├── __init__.py
├── admin.py            # Admin interface
├── apps.py             # App configuration
├── models.py           # Data models
├── views.py            # View logic
├── urls.py             # URL patterns
├── forms.py            # Django forms
├── serializers.py      # DRF serializers (if --api)
├── templates/blog/     # HTML templates
├── migrations/         # Database migrations
├── management/
│   └── commands/
│       └── seed.py     # Seed command (if --seed)
└── tests/
    ├── test_models.py
    ├── test_views.py
    └── test_api.py
```

### Scaffolding Features

Add specific features to existing apps:

```bash
corex scaffold FEATURE --app=APP_NAME [OPTIONS]
```

**Available Features:**
- `model` - Add new models
- `view` - Add views for existing models
- `api` - Add API endpoints
- `form` - Add Django forms
- `admin` - Add admin interface

**Examples:**

```bash
# Add a new model to blog app
corex scaffold model --app=blog --model=Comment --fields="content:text,author:str,post:fk"

# Add API endpoints to existing app
corex scaffold api --app=blog --model=Post

# Add custom views
corex scaffold view --app=blog --model=Post
```

### Generating Demo Data

Populate your apps with demo data:

```bash
# Generate data for all apps
corex seed --count=50

# Generate data for specific app
corex seed --app=blog --count=20
```

---

## Advanced Features

### Health Checks

Monitor your project health:

```bash
# Comprehensive health check
corex doctor

# Output includes:
# ✅ Python 3.11.0
# ✅ Django 4.2.0
# ✅ Database connection
# ✅ Migrations up to date
# ⚠️  Missing: Redis connection

# Auto-fix common issues
corex doctor --fix
```

**What `doctor` checks:**
- Python and Django versions
- Database connectivity
- Migration status
- Static files collection
- Required directories
- Environment configuration

### Service Integrations

Add external services to your project:

```bash
# Payment processing
corex integrate stripe

# File storage
corex integrate s3

# Search functionality
corex integrate elasticsearch

# Background tasks
corex integrate celery

# Email services
corex integrate email

# Caching and sessions
corex integrate redis
```

### CI/CD Setup

Initialize automated CI/CD pipelines:

```bash
# GitHub Actions
corex ci --github

# GitLab CI
corex ci --gitlab

# With Docker builds
corex ci --github --docker
```

**Generated CI Features:**
- Automated testing
- Code quality checks
- Security scanning
- Docker image building
- Deployment automation

### Deployment

Deploy your Django projects directly to popular cloud platforms with a single command:

```bash
corex deploy --platform=PLATFORM [OPTIONS]
```

**Supported Platforms:**
- **Vercel**: Zero-config deployments with global CDN
- **Railway**: Infrastructure platform with automatic scaling
- **Render**: Full-stack cloud platform with managed databases
- **Heroku**: Cloud application platform

**Available Options:**

| Option | Description | Example |
|--------|-------------|----------|
| `--platform` | Target platform (required) | `--platform=vercel` |
| `--env-file` | Environment file to use | `--env-file=.env.prod` |
| `--auto-db` | Auto-provision database | `--auto-db` |
| `--domain` | Custom domain name | `--domain=myapp.com` |
| `--region` | Deployment region | `--region=us-east-1` |
| `--force` | Force deployment | `--force` |

**Platform-Specific Examples:**

```bash
# Deploy to Vercel (serverless)
corex deploy --platform=vercel

# Deploy to Railway with PostgreSQL
corex deploy --platform=railway --auto-db --region=us-west1

# Deploy to Render with custom domain
corex deploy --platform=render --auto-db --domain=myapp.render.com

# Deploy to Heroku with custom region
corex deploy --platform=heroku --auto-db --region=eu
```

**What the deploy command does:**
1. **Health Check**: Validates project structure and dependencies
2. **Configuration Generation**: Creates platform-specific config files
3. **Environment Setup**: Processes .env variables for deployment
4. **Database Provisioning**: Sets up PostgreSQL (if --auto-db)
5. **Deployment**: Executes platform-specific deployment commands
6. **Status Reporting**: Shows deployment logs and final URL

**Generated Files:**
- **Vercel**: `vercel.json`, deployment configuration
- **Railway**: `railway.toml`, `Procfile`
- **Render**: `render.yaml`, `build.sh`
- **Heroku**: `Procfile`, `runtime.txt`, `release.sh`
- **Common**: `Dockerfile`, updated `requirements.txt`

---

## Configuration Options

### Authentication Methods

**Session Authentication (Default)**
```bash
corex new myproject --auth=session
```
- Traditional Django sessions
- Server-side state management
- Built-in CSRF protection
- Best for: Traditional web applications

**JWT Authentication**
```bash
corex new myproject --auth=jwt
```
- JSON Web Tokens
- Stateless authentication
- Mobile app friendly
- Best for: APIs, SPAs, mobile apps

**Social Authentication**
```bash
corex new myproject --auth=allauth
```
- OAuth integration
- Multiple providers (Google, GitHub, etc.)
- Social login support
- Best for: User-facing applications

### UI Frameworks

**Tailwind CSS (Default)**
```bash
corex new myproject --ui=tailwind
```
- Utility-first CSS framework
- Modern, responsive design
- Alpine.js integration
- Fast development

**Bootstrap**
```bash
corex new myproject --ui=bootstrap
```
- Component-based framework
- Familiar and stable
- jQuery integration
- Rapid prototyping

**No Framework**
```bash
corex new myproject --ui=none
```
- API-only projects
- Custom frontend frameworks
- Maximum flexibility

### Database Options

**PostgreSQL**
```bash
corex new myproject --database=postgres
```
- Production-ready
- Advanced features
- Best performance
- JSON support

**MySQL**
```bash
corex new myproject --database=mysql
```
- Wide hosting support
- Traditional choice
- Good performance
- Mature ecosystem

**SQLite (Default)**
```bash
corex new myproject --database=sqlite
```
- Zero configuration
- Perfect for development
- Single file database
- Easy deployment

---

## Testing & Development

### Running Tests

```bash
# Run all tests
corex test

# Run tests with coverage
corex test --coverage
# ✅ Generates htmlcov/index.html

# Run tests in parallel
corex test --parallel

# Test specific app
corex test blog

# Combined options
corex test blog --coverage --parallel
```

**Generated Test Types:**
- **Model Tests**: Validation, methods, relationships
- **View Tests**: Response codes, permissions, context
- **API Tests**: Endpoints, serialization, authentication
- **Integration Tests**: User workflows, end-to-end scenarios

**Coverage Reports:**
- Terminal summary
- HTML report at `htmlcov/index.html`
- Detailed line-by-line coverage
- Missing line identification

---

## Deployment & CI/CD

### Docker Support

Every CoreX project includes Docker configuration:

```bash
# Development
corex runserver --docker

# Production
docker-compose -f docker-compose.prod.yml up --build
```

**Included Services:**
- Web application (Django + Gunicorn)
- Database (PostgreSQL/MySQL)
- Redis (caching and sessions)
- Celery (background tasks)

### Environment Configuration

Generated `.env` files include:

```bash
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=myproject
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# External Services
REDIS_URL=redis://localhost:6379/1
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Production Deployment

CoreX projects are ready for:

- **Heroku**: `git push heroku main`
- **AWS**: ECS, EC2, Elastic Beanstalk
- **Google Cloud**: Cloud Run, Compute Engine
- **DigitalOcean**: App Platform, Droplets
- **VPS**: Docker Compose + Nginx

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
corex runserver --port=8001
```

**Missing dependencies:**
```bash
corex doctor --fix
poetry install
```

**Database connection errors:**
```bash
# Check .env configuration
# Ensure database server is running
corex doctor
```

**Migration errors:**
```bash
# Reset migrations (development only)
rm -rf app/migrations/
python3 manage.py makemigrations app
python3 manage.py migrate
```

**Template not found:**
```bash
# Reinstall CoreX
pip install --upgrade corex
```

### Environment Issues

**Poetry not found:**
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

**Docker not found:**
```bash
# Install Docker Desktop
# Visit: https://docs.docker.com/get-docker/
```

**Permission errors:**
```bash
# Fix file permissions
chmod +x manage.py
```

---

## Examples & Workflows

### Complete Blog Development

```bash
# 1. Create project
corex new myblog --auth=session --ui=tailwind --database=postgres

# 2. Enter project
cd myblog

# 3. Create blog app
corex app blog --type=blog --seed --api

# 4. Run migrations
corex migrate

# 5. Create admin user
corex createsuperuser

# 6. Start server
corex runserver

# 7. Visit admin: http://localhost:8000/admin/
# 8. Visit blog: http://localhost:8000/blog/
```

### E-commerce Platform

```bash
# 1. Create project with JWT and Docker
corex new eshop --auth=jwt --ui=tailwind --database=postgres --docker --api

# 2. Create shop app
corex app products --type=shop --api

# 3. Add customer management
corex app customers --type=crm

# 4. Generate demo data
corex seed --count=100

# 5. Run with Docker
corex runserver --docker
```

### API-Only Service

```bash
# 1. Create API project
corex new api --auth=jwt --ui=none --database=postgres --api

# 2. Create apps
corex app users --api
corex app content --type=blog --api

# 3. Setup CI/CD
corex ci --github --docker

# 4. Integrate services
corex integrate redis
corex integrate celery
```

### Multi-App Platform

```bash
# 1. Create platform
corex new platform --auth=allauth --ui=tailwind --database=postgres --docker --api

# 2. Add multiple apps
corex app blog --type=blog --api
corex app shop --type=shop --api
corex app community --type=social --api
corex app support --type=forum --api

# 3. Generate comprehensive test data
corex seed --count=50

# 4. Setup monitoring
corex doctor

# 5. Deploy
corex ci --github --docker
```

### Development Workflow

```bash
# Daily development workflow

# 1. Check project health
corex doctor

# 2. Add new feature
corex scaffold model --app=blog --model=Category

# 3. Run tests
corex test blog --coverage

# 4. Seed data for testing
corex seed --app=blog --count=10

# 5. Start development
corex runserver
```

---

## Command Reference Quick Guide

| Command | Purpose | Example |
|---------|---------|---------|
| `corex new` | Create project | `corex new blog --auth=jwt` |
| `corex app` | Generate app | `corex app store --type=shop` |
| `corex scaffold` | Add features | `corex scaffold api --app=blog` |
| `corex runserver` | Start server | `corex runserver --docker` |
| `corex migrate` | Run migrations | `corex migrate --app=blog` |
| `corex test` | Run tests | `corex test --coverage` |
| `corex seed` | Generate data | `corex seed --count=50` |
| `corex doctor` | Health check | `corex doctor --fix` |
| `corex ci` | Setup CI/CD | `corex ci --github` |
| `corex integrate` | Add services | `corex integrate stripe` |

---

**Happy coding with CoreX! 🚀**

For more help:
- Run `corex COMMAND --help` for command-specific help
- Check `corex doctor` for environment issues
- Visit the documentation for advanced topics