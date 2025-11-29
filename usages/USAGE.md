# CoreX Usage Guide

Comprehensive documentation for the CoreX Django scaffolding framework.

## 🚀 Getting Started

### Installation

```bash
# Install CoreX globally
pip install corex

# Or install in development mode
git clone https://github.com/yourusername/corex.git
cd corex
pip install -e .
```

### Creating Projects

Generate production-ready Django projects with a single command:

```bash
# Basic project
corex new myproject

# Full-featured project
corex new ecommerce --auth=jwt --ui=tailwind --database=postgres --docker --api

# API-only project
corex new api_service --auth=jwt --ui=none --database=postgres --api
```

**Project Creation Options:**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--auth` | `jwt`, `session`, `allauth` | `session` | Authentication method |
| `--ui` | `tailwind`, `bootstrap`, `none` | `tailwind` | UI framework |
| `--database` | `postgres`, `mysql`, `sqlite` | `sqlite` | Database backend |
| `--docker` | flag | disabled | Include Docker configuration |
| `--api` | flag | disabled | Include Django REST Framework |

---

## 🏗️ App Development

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
| `education` | Education Management | Student, Instructor, Course, Enrollment, Grade, Attendance | Course management, grade tracking, attendance |
| `fintech` | Financial Technology | Account, Transaction, Budget, Invoice, Investment | Financial tracking, budgeting, investments |
| `healthcare` | Healthcare Management | Patient, Provider, Appointment, Record, Medication | Patient management, scheduling, medical records |

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

# Create an education management system
corex app lms --type=education --seed

# Create a financial management system
corex app finance --type=fintech --api

# Create a healthcare management system
corex app clinic --type=healthcare --auth=jwt
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
- **Railway**: Full-stack deployments with database provisioning
- **Render**: Simple deployments with custom domains
- **Heroku**: Traditional PaaS with extensive ecosystem

**Deployment Options:**

| Option | Description |
|--------|-------------|
| `--platform` | Target platform (vercel, railway, render, heroku) |
| `--env-file` | Environment file to use (default: .env) |
| `--auto-db` | Automatically provision database |
| `--domain` | Custom domain name |
| `--region` | Deployment region |
| `--force` | Force deployment even if checks fail |

**Examples:**

```bash
# Deploy to Vercel
corex deploy --platform=vercel --domain=myapp.example.com

# Deploy to Railway with auto-provisioned database
corex deploy --platform=railway --auto-db --region=us-west

# Deploy to Heroku
corex deploy --platform=heroku --env-file=.env.prod
```

---

## 🧪 Testing & Development

### Running Tests

Execute comprehensive test suites:

```bash
# Run all tests
corex test

# Run tests for specific app
corex test blog

# Run tests with coverage
corex test --coverage

# Run tests in parallel
corex test --parallel
```

### Development Server

Start the development server with optional Docker support:

```bash
# Standard development server
corex runserver

# With Docker
corex runserver --docker

# Custom port and host
corex runserver --port=8001 --host=0.0.0.0
```

### Database Management

Manage your database with convenience commands:

```bash
# Run migrations
corex migrate

# Run migrations for specific app
corex migrate --app=blog

# Mark migrations as applied without running
corex migrate --fake
```

### User Management

Create and manage Django users:

```bash
# Create superuser interactively
corex createsuperuser

# Create superuser with predefined credentials
corex createsuperuser --username=admin --email=admin@example.com --noinput
```

---

## 🛠️ Configuration & Customization

### Environment Variables

CoreX projects use environment variables for configuration:

```bash
# Example .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Custom Templates

Extend CoreX with custom app templates:

1. Create templates in `corex/templates/apps/types/`
2. Add models in `corex/templates/apps/models.py.j2`
3. Add views in `corex/templates/apps/views.py.j2`
4. Update tests in `test_corex.py`
5. Submit a pull request

### Project Structure

CoreX generates well-organized Django projects:

```
myproject/
├── manage.py
├── pyproject.toml
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── Dockerfile
├── docker-compose.yml
├── static/
├── media/
├── templates/
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── apps/
    └── ... (generated apps)
```

---

## 📚 Industry-Specific Templates

CoreX provides specialized templates for key industries:

### Education
Perfect for Learning Management Systems (LMS) and educational platforms:
- Student and instructor management
- Course catalog and enrollment
- Grade tracking and attendance
- Assignments and submissions
- Announcements and resources

### Fintech
Ideal for financial applications and payment systems:
- Account and transaction management
- Budgeting and financial tracking
- Invoicing and billing
- Investment portfolio tracking
- Financial goal planning

### Healthcare
Designed for medical and healthcare applications:
- Patient and provider management
- Appointment scheduling
- Medical records and prescriptions
- Billing and insurance
- Vaccination tracking

---

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

---

## 🤝 Contributing

We welcome contributions to CoreX! Here's how you can help:

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/corex.git
cd corex

# Install in development mode
pip install -e .

# Run tests
python -m pytest
```

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write tests for new features
5. Update documentation
6. Submit a pull request

### Areas for Contribution
- New app templates
- Additional authentication methods
- More UI frameworks
- Extended database support
- Additional deployment platforms
- GUI enhancements
- Documentation improvements

---

## 🆘 Troubleshooting

### Common Issues

**Docker Permission Errors**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

**Database Connection Issues**
```bash
# Check database service status
corex doctor
# Verify DATABASE_URL in .env
```

**Missing Dependencies**
```bash
# Install missing packages
pip install -r requirements.txt
# Or use Poetry
poetry install
```

### Getting Help

- Check the [GitHub Issues](https://github.com/yourusername/corex/issues)
- Join our [Discord Community](https://discord.gg/corex)
- Read the [API Reference](API_REFERENCE.md)
- View [Release Notes](RELEASE_NOTES.md)

---

## 📄 License

CoreX is released under the MIT License. See [LICENSE](LICENSE) for details.

---

*CoreX - Streamline Django Development*