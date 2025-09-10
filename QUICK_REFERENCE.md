# CoreX Quick Reference

**Essential commands and options for rapid Django development with CoreX**

## 🚀 Essential Commands

### New Project
```bash
corex new PROJECT_NAME [OPTIONS]

# Options:
--auth     jwt|session|allauth      # Authentication method (default: session)
--ui       tailwind|bootstrap|none  # UI framework (default: tailwind)  
--database postgres|mysql|sqlite    # Database (default: sqlite)
--docker                           # Include Docker config
--api                              # Include DRF API setup
```

### Generate App
```bash
corex app APP_NAME --type=TYPE [OPTIONS]

# Types: blog, shop, wiki, crm, social, forum, portfolio, elearn
# Options: --seed, --api, --auth, --ui
```

### Development Server
```bash
corex runserver [OPTIONS]

# Options:
--docker          # Run with Docker
--port INTEGER    # Port (default: 8000)
--host TEXT       # Host (default: 127.0.0.1)
```

## 📋 Command Matrix

| Task | Command | Example |
|------|---------|---------|
| **Create blog project** | `corex new PROJECT --auth=TYPE` | `corex new myblog --auth=jwt --ui=tailwind` |
| **Create shop app** | `corex app APP --type=shop` | `corex app store --type=shop --api` |
| **Run server** | `corex runserver` | `corex runserver --docker --port=8001` |
| **Run migrations** | `corex migrate` | `corex migrate --app=blog` |
| **Run tests** | `corex test` | `corex test blog --coverage` |
| **Create admin** | `corex createsuperuser` | `corex createsuperuser --username=admin` |
| **Generate data** | `corex seed` | `corex seed --app=blog --count=50` |
| **Health check** | `corex doctor` | `corex doctor --fix` |
| **Setup CI/CD** | `corex ci` | `corex ci --github --docker` |
| **Add services** | `corex integrate SERVICE` | `corex integrate stripe` |
| **Deploy project** | `corex deploy --platform=PLATFORM` | `corex deploy --platform=vercel --auto-db` |

## 🏗️ App Types & Use Cases

| Type | Models | Best For | API | Seed Data |
|------|--------|----------|-----|-----------|
| `blog` | Post, Comment, Category | Content sites, news | ✅ | ✅ |
| `shop` | Product, Order, Cart | E-commerce | ✅ | ✅ |
| `wiki` | Page, Revision | Documentation | ✅ | ✅ |
| `crm` | Contact, Deal, Task | Sales management | ✅ | ✅ |
| `social` | Profile, Post, Follow | Social networks | ✅ | ✅ |
| `forum` | Topic, Post, Category | Discussion boards | ✅ | ✅ |
| `portfolio` | Project, Skill | Personal sites | ✅ | ✅ |
| `elearn` | Course, Lesson | Education platforms | ✅ | ✅ |

## ⚙️ Configuration Quick Pick

### Authentication
```bash
# Traditional web apps
--auth=session

# APIs and SPAs  
--auth=jwt

# Social login
--auth=allauth
```

### UI Framework
```bash
# Modern utility-first
--ui=tailwind

# Component-based
--ui=bootstrap  

# API-only
--ui=none
```

### Database
```bash
# Development
--database=sqlite

# Production
--database=postgres

# Shared hosting
--database=mysql
```

## 🔄 Common Workflows

### Blog Site (5 minutes)
```bash
corex new myblog --auth=session --ui=tailwind
cd myblog
corex app blog --type=blog --seed
corex migrate
corex createsuperuser
corex runserver
```

### E-commerce Platform
```bash
corex new eshop --auth=jwt --database=postgres --docker --api
cd eshop  
corex app products --type=shop --api --seed
corex app customers --type=crm
corex runserver --docker
```

### API Service
```bash
corex new api --auth=jwt --ui=none --database=postgres --api
cd api
corex app content --type=blog --api
corex integrate redis
corex ci --github --docker
```

### Multi-App Platform
```bash
corex new platform --auth=allauth --ui=tailwind --docker --api
cd platform
corex app blog --type=blog --api
corex app shop --type=shop --api  
corex app community --type=social
corex seed --count=100
```

## 🛠️ Development Tips

### Daily Commands
```bash
corex doctor              # Check health
corex test --coverage     # Run tests
corex seed --count=10     # Fresh test data
corex runserver          # Start development
```

### Troubleshooting
```bash
corex doctor --fix       # Auto-fix issues
corex runserver --port=8001  # Port conflicts
corex migrate --fake     # Migration issues
pip install --upgrade corex  # Update CoreX
```

### Testing
```bash
corex test               # All tests
corex test blog          # Specific app
corex test --parallel    # Faster execution  
corex test --coverage    # With coverage report
```

## 📁 Project Structure Preview

```
myproject/
├── myproject/          # Django project
├── blog/              # Generated apps
├── static/            # Static files
├── templates/         # HTML templates
├── media/             # User uploads
├── manage.py          # Django management
├── pyproject.toml     # Dependencies
├── Dockerfile         # Container config
├── docker-compose.yml # Services
├── .env               # Environment vars
└── README.md          # Documentation
```

## ⚡ Performance Tips

- Use `--parallel` for faster tests
- Use `--docker` for consistent environments  
- Use `--seed` to generate test data quickly
- Use `corex doctor` to catch issues early
- Use `--api` for frontend decoupling

## 🚨 Common Gotchas

1. **Port conflicts**: Use `--port=8001` 
2. **Missing deps**: Run `corex doctor --fix`
3. **DB issues**: Check `.env` configuration
4. **Migration errors**: Use `--fake` flag carefully
5. **Permission errors**: Check file permissions

## 🔗 Integration Services

| Service | Command | Purpose |
|---------|---------|---------|
| Stripe | `corex integrate stripe` | Payments |
| AWS S3 | `corex integrate s3` | File storage |
| Redis | `corex integrate redis` | Caching |
| Celery | `corex integrate celery` | Background tasks |
| Elasticsearch | `corex integrate elasticsearch` | Search |
| Email | `corex integrate email` | Email services |

## 📊 CI/CD Options

```bash
# GitHub Actions
corex ci --github

# GitLab CI  
corex ci --gitlab

# With Docker builds
corex ci --github --docker
```

## 🚀 Deployment Options

```bash
# Deploy to Vercel
corex deploy --platform=vercel

# Deploy to Railway with auto database
corex deploy --platform=railway --auto-db

# Deploy to Render with custom domain
corex deploy --platform=render --domain=myapp.com

# Deploy to Heroku with region
corex deploy --platform=heroku --region=us
```

---

**Need help?** Run `corex COMMAND --help` for detailed options!