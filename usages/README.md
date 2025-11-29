# CoreX 🚀

**The Ultimate Django Scaffolding Framework for Rapid Application Development**

[![PyPI version](https://badge.fury.io/py/corex.svg)](https://badge.fury.io/py/corex)
[![Python versions](https://img.shields.io/pypi/pyversions/corex.svg)](https://pypi.org/project/corex/)
[![Django versions](https://img.shields.io/badge/django-4.2%2B-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](https://github.com/ramazon07-cmd/corex)

CoreX is a comprehensive Django scaffolding framework that combines the simplicity of Rails generators, the flexibility of Laravel Artisan, and modern tooling like Poetry and Docker. Generate production-ready Django applications with a single command.

## 🎯 Why CoreX?

- **⚡ Lightning Fast**: Create complete Django projects in seconds
- **🔧 Production Ready**: Generated code follows Django best practices
- **🎨 Modern UI**: Built-in Tailwind CSS and Bootstrap support
- **🔐 Authentication**: JWT, Session, and Social auth out of the box
- **📱 API First**: Django REST Framework integration
- **🐳 Docker Ready**: Container configuration included
- **🚀 CI/CD**: GitHub Actions and GitLab CI templates
- **🧪 Test Included**: Comprehensive test suites generated
- **📊 Multiple DBs**: PostgreSQL, MySQL, SQLite support

## 🚀 Quick Start

### Installation

```
# Install CoreX
pip install corex

# Verify installation
corex --version
```

### Create Your First Project

```
# Create a new Django project with JWT auth and Tailwind UI
corex new myproject --auth=jwt --ui=tailwind --database=postgres

# Navigate to the project
cd myproject

# Start the development server
corex runserver
```

That's it! You now have a fully configured Django project with:
- JWT Authentication
- Tailwind CSS styling
- PostgreSQL database
- Docker configuration
- API endpoints
- Admin interface
- Environment configuration

## 📋 Core Commands

### Project Management

```
# Create a new project
corex new <project_name> [OPTIONS]

# Options:
#   --auth: jwt|session|allauth (default: session)
#   --ui: tailwind|bootstrap|none (default: tailwind)
#   --database: postgres|mysql|sqlite (default: sqlite)
#   --docker: Include Docker configuration
#   --api: Include DRF API setup

# Examples:
corex new blog --auth=allauth --ui=bootstrap --database=mysql --docker
corex new ecommerce --auth=jwt --ui=tailwind --database=postgres --api
```

### App Generation

```
# Generate specialized apps
corex app <app_name> --type=<type> [OPTIONS]

# Available app types:
corex app blog --type=blog        # Blog with posts, comments, categories
corex app store --type=shop       # E-commerce with products, orders
corex app docs --type=wiki        # Wiki with pages and revisions
corex app sales --type=crm        # CRM with contacts and deals
corex app community --type=social # Social network features
corex app discussion --type=forum # Forum with topics and posts

# Options:
#   --seed: Generate demo data
#   --api: Include API endpoints
#   --auth: Override project auth
#   --ui: Override project UI
```

### Development Commands

```
# Server management
corex runserver                   # Start development server
corex runserver --docker          # Start with Docker
corex runserver --port=8001       # Custom port

# Database operations
corex migrate                      # Run migrations
corex migrate --app=myapp         # App-specific migrations
corex createsuperuser             # Create admin user

# Testing
corex test                        # Run all tests
corex test --coverage             # Run with coverage report
corex test --app=myapp            # Test specific app
corex test --parallel             # Parallel test execution

# Data management
corex seed                        # Generate demo data
corex seed --app=blog --count=50  # Generate 50 blog posts
```

### DevOps & Utilities

```
# CI/CD setup
corex ci init --github            # GitHub Actions
corex ci init --gitlab            # GitLab CI
corex ci init --github --docker   # With Docker builds

# Service integrations
corex integrate stripe            # Payment processing
corex integrate s3                # File storage
corex integrate elasticsearch     # Search functionality
corex integrate redis             # Caching and sessions
corex integrate celery            # Background tasks
corex integrate email             # Email configuration

# Project health
corex doctor                      # Check project health
corex doctor --fix                # Auto-fix common issues

# Advanced scaffolding
corex scaffold model --model=Product --fields="name:str,price:decimal"
corex scaffold view --model=Product
corex scaffold api --model=Product
```

## 🖥️ GUI Version

CoreX now includes a Graphical User Interface for visual project configuration:

### Features
- Visual project creation wizard
- Template selection with previews
- Configuration options without CLI
- Real-time command execution feedback
- Cross-platform support (Web, Desktop)

### Getting Started with GUI
1. Navigate to the GUI directory: `cd gui/corex-gui`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Open your browser to: `http://localhost:3000`

### GUI Capabilities
- Create new Django projects with visual configuration
- Generate specialized apps with template selection
- Configure authentication, UI framework, and database options
- Enable Docker and API features with checkboxes
- View command execution results in real-time

## 🏗️ App Types & Features

CoreX provides specialized app templates with complete functionality:

### 📝 Blog App
- **Models**: Posts, Comments, Categories, Tags
- **Features**: Rich text editor, SEO optimization, social sharing
- **API**: Full CRUD operations, filtering, search
- **Templates**: Post list, detail, category pages

```bash
corex app blog --type=blog --seed
# ✅ Creates complete blog with demo content
```

### 🛍️ Shop App
- **Models**: Products, Orders, Categories, Cart
- **Features**: Inventory management, payment integration
- **API**: Product catalog, order management
- **Templates**: Product grid, detail, cart pages

```bash
corex app store --type=shop --api
# ✅ Creates e-commerce backend with API
```

### 📚 Wiki App
- **Models**: Pages, Revisions, Categories
- **Features**: Version control, Markdown support, search
- **API**: Page management, revision history
- **Templates**: Page view, edit, history

```bash
corex app docs --type=wiki --ui=tailwind
# ✅ Creates documentation wiki
```

### 💼 CRM App
- **Models**: Contacts, Deals, Tasks, Companies
- **Features**: Pipeline management, activity tracking
- **API**: Contact management, deal tracking
- **Templates**: Dashboard, contact list, deal pipeline

```bash
corex app sales --type=crm --auth=jwt
# ✅ Creates sales CRM system
```

### 👥 Social App
- **Models**: Profiles, Posts, Follows, Likes
- **Features**: Activity feeds, messaging, notifications
- **API**: Social interactions, feed generation
- **Templates**: Profile, feed, messaging

```bash
corex app community --type=social --seed
# ✅ Creates social network features
```

### 💬 Forum App
- **Models**: Topics, Posts, Categories
- **Features**: Moderation tools, user reputation
- **API**: Topic management, post threading
- **Templates**: Topic list, discussion view

```bash
corex app discussion --type=forum
# ✅ Creates discussion forum
```

### 🎓 Education App
- **Models**: Students, Instructors, Courses, Enrollments, Assignments, Grades, Attendance
- **Features**: Course management, grade tracking, attendance, certificates
- **API**: Student management, course enrollment, grade reporting
- **Templates**: Course catalog, student dashboard, grade reports

```bash
corex app lms --type=education --seed
# ✅ Creates learning management system
```

### 💰 Fintech App
- **Models**: Accounts, Transactions, Budgets, Invoices, Investments, Financial Goals
- **Features**: Financial tracking, budgeting, invoicing, investment management
- **API**: Account management, transaction processing, financial reporting
- **Templates**: Dashboard, transaction history, budget planning

```bash
corex app finance --type=fintech --api
# ✅ Creates financial management system
```

### 🏥 Healthcare App
- **Models**: Patients, Providers, Appointments, Medical Records, Prescriptions, Medications, Vital Signs
- **Features**: Patient management, appointment scheduling, medical records, medication tracking
- **API**: Patient records, appointment booking, prescription management
- **Templates**: Patient portal, provider dashboard, appointment calendar

```bash
corex app clinic --type=healthcare --auth=jwt
# ✅ Creates healthcare management system
```

## 🔧 Configuration Options

### Authentication Options

| Option | Description | Features |
|--------|-------------|----------|
| `jwt` | JSON Web Tokens | Stateless, API-friendly, mobile apps |
| `session` | Django Sessions | Traditional web apps, server-side |
| `allauth` | Social Authentication | OAuth, multiple providers, social login |

### UI Framework Options

| Option | Description | Best For |
|--------|-------------|----------|
| `tailwind` | Tailwind CSS + Alpine.js | Modern, utility-first styling |
| `bootstrap` | Bootstrap 5 + jQuery | Rapid prototyping, familiar |
| `none` | No frontend framework | API-only, custom frontend |

### Database Options

| Option | Description | Use Case |
|--------|-------------|----------|
| `postgres` | PostgreSQL | Production, advanced features |
| `mysql` | MySQL/MariaDB | Traditional web hosting |
| `sqlite` | SQLite | Development, simple deployments |

## 🐳 Docker Support

CoreX projects come with production-ready Docker configuration:

```
# Development with Docker
corex runserver --docker

# Production deployment
docker-compose -f docker-compose.prod.yml up --build

# Services included:
# - Web application (Django + Gunicorn)
# - Database (PostgreSQL/MySQL)
# - Redis (caching and sessions)
# - Celery (background tasks)
```

## 🧪 Testing & Quality

Generated projects include comprehensive testing:

```
# Run all tests
corex test

# Coverage reporting
corex test --coverage
# ✅ Generates HTML coverage report at htmlcov/index.html

# Parallel testing
corex test --parallel

# Specific app testing
corex test blog
```

**Generated test types:**
- Model tests (validation, methods, relationships)
- View tests (responses, permissions, forms)
- API tests (endpoints, serialization, authentication)
- Integration tests (workflows, user journeys)

## 🚀 Deployment & CI/CD

### Automated CI/CD Setup

```
# GitHub Actions
corex ci init --github
# ✅ Creates .github/workflows/ci.yml
# ✅ Includes testing, linting, building, deployment

# GitLab CI
corex ci init --gitlab
# ✅ Creates .gitlab-ci.yml
# ✅ Includes security scanning, Docker builds
```

### Production Deployment

Generated projects are deployment-ready for:

- **Heroku**: `git push heroku main`
- **AWS**: ECS, EC2, Elastic Beanstalk
- **Google Cloud**: Cloud Run, Compute Engine
- **DigitalOcean**: App Platform, Droplets
- **VPS**: Docker Compose + Nginx

## 🔌 Service Integrations

Add popular services with one command:

```
# Payment processing
corex integrate stripe
# ✅ Payment views, webhooks, models

# File storage
corex integrate s3
# ✅ AWS S3 configuration, media handling

# Search functionality
corex integrate elasticsearch
# ✅ Search views, indexing, configurations

# Background tasks
corex integrate celery
# ✅ Task queue, periodic tasks, monitoring

# Email services
corex integrate email
# ✅ SMTP configuration, templates, utilities
```

## 📁 Project Structure

Generated projects follow Django best practices:

```
myproject/
├── myproject/              # Main project directory
│   ├── settings.py         # Environment-based settings
│   ├── urls.py            # URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── apps/                   # Generated apps
│   ├── blog/              # Blog app
│   ├── shop/              # Shop app
│   └── api/               # API endpoints
├── static/                 # Static files
├── media/                  # User uploads
├── templates/              # HTML templates
├── tests/                  # Test files
├── docs/                   # Documentation
├── docker-compose.yml      # Docker configuration
├── Dockerfile             # Docker image
├── pyproject.toml         # Dependencies (Poetry)
├── requirements.txt       # Pip requirements
├── .env                   # Environment variables
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🛠️ Advanced Usage

### Custom Templates

Create your own app templates:

```
# Create custom template directory
mkdir -p ~/.corex/templates/custom_app

# Add your Jinja2 templates
# Use CoreX template variables: {{ app_name }}, {{ auth }}, {{ ui }}

# Use custom template
corex app myapp --template=custom_app
```

### Environment Configuration

Generated `.env` files include:

```
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
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

### Health Monitoring

```
# Comprehensive health check
corex doctor

# Sample output:
# ✅ Python 3.11.0
# ✅ Django 4.2.0
# ✅ Database connection
# ✅ Migrations up to date
# ✅ Static files collected
# ⚠️  Missing: Redis connection

# Auto-fix common issues
corex doctor --fix
# ✅ Created missing directories
# ✅ Applied pending migrations
# ✅ Collected static files
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```
# Clone the repository
git clone https://github.com/ramazon07-cmd/corex.git
cd corex

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Install in development mode
poetry run pip install -e .
```

### Adding New App Types

1. Create templates in `corex/templates/apps/types/`
2. Add models in `corex/templates/apps/models.py.j2`
3. Add views in `corex/templates/apps/views.py.j2`
4. Update tests in `test_corex.py`
5. Submit a pull request

## 📚 Documentation

- **Full Documentation**: [docs.corex.dev](https://docs.corex.dev)
- **API Reference**: [api.corex.dev](https://api.corex.dev)
- **Tutorial Videos**: [youtube.com/corexdev](https://youtube.com/corexdev)
- **Community**: [discord.gg/corex](https://discord.gg/corex)

## 🐛 Troubleshooting

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

**Template not found:**
```bash
# Reinstall CoreX
pip install --upgrade corex
```

## 📊 Performance & Benchmarks

| Operation | Time | Generated Files |
|-----------|------|----------------|
| Create Project | ~15s | 25+ files |
| Add Blog App | ~3s | 15+ files |
| Run Tests | ~5s | 100% coverage |
| Build Docker | ~2m | Multi-stage build |

## 🔄 Migration from Other Tools

### From Django Startproject

```
# Instead of:
django-admin startproject myproject
python3 manage.py startapp myapp

# Use CoreX:
corex new myproject --auth=session --ui=bootstrap
corex app myapp --type=blog
```

### From Cookiecutter Django

```
# Instead of:
cookiecutter https://github.com/cookiecutter/cookiecutter-django

# Use CoreX:
corex new myproject --auth=allauth --ui=tailwind --docker
```

## 🔮 Roadmap

- [ ] **v1.1**: React/Vue.js frontend templates
- [ ] **v1.2**: GraphQL API support
- [ ] **v1.3**: Kubernetes deployment
- [ ] **v1.4**: AI-powered code generation
- [ ] **v1.5**: Real-time features (WebSockets)

## 📄 License

CoreX is released under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Inspired by Rails generators and Laravel Artisan
- Built on the shoulders of Django and the Python community
- Thanks to all contributors and users

---

⭐ **Star this repository if CoreX helps you build amazing Django applications!**

Made with ❤️ by the CoreX team
