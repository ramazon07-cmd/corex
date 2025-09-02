# CoreX 🚀

A comprehensive Django scaffolding framework for rapid application development, inspired by Rails generators and Laravel Artisan.

## 🎯 Vision

Make CoreX the go-to Django scaffolding framework, combining:
- The simplicity of Rails generators
- The flexibility of Laravel Artisan  
- The modern tooling of Poetry + Docker
- Tailored for Django + DRF developers

## 🛠️ Core Features

### Project Creation
```bash
corex new <project_name> --auth=jwt|session|allauth --ui=tailwind|bootstrap|none
```

Creates a fully configured Django project with:
- Poetry + Docker + .env
- Postgres + Redis setup
- DRF integration
- Optional auth and UI packages

### App Scaffolding
```bash
corex app <app_name> --type=<blog|portfolio|forum|wiki|elearn|social|crm|shop>
```

Generates apps with:
- Models (with sensible defaults & relationships)
- Admin registrations
- URLs + Views / DRF APIs
- Templates (Tailwind support if UI enabled)
- Serializers (if API enabled)
- Seeds / demo data (--seed)
- Unit tests (basic CRUD + model tests)

### Example Usage
```bash
corex app blog --auth=jwt --ui=tailwind
```
→ Generates a complete blog app with posts, comments, templates, admin, and JWT authentication.

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/corex.git
cd corex

# Install with Poetry
poetry install

# Install CoreX globally
poetry build
pip install dist/corex-0.1.0.tar.gz
```

### Create Your First Project
```bash
# Create a new Django project with JWT auth and Tailwind UI
corex new myproject --auth=jwt --ui=tailwind

# Navigate to the project
cd myproject

# Start the development server
corex runserver
```

## 📋 Available Commands

### Project Management
- `corex new <project_name>` - Create a new Django project
- `corex runserver [--docker]` - Run development server
- `corex migrate` - Run database migrations
- `corex createsuperuser` - Create admin user
- `corex test` - Run tests

### App Development
- `corex app <app_name>` - Generate a new app
- `corex scaffold <feature>` - Add new models/views to an app
- `corex seed` - Generate demo data

### DevOps & Integrations
- `corex ci init [--github|--gitlab]` - Generate CI/CD pipelines
- `corex integrate <service>` - Add integrations (Stripe, S3, ElasticSearch, Redis)
- `corex doctor` - Check environment health

## 🏗️ App Types

CoreX supports various app types with pre-configured models and functionality:

### Blog
- Posts, Comments, Categories, Tags
- Rich text editor support
- SEO optimization
- Social sharing

### Portfolio
- Projects, Skills, Testimonials
- Image galleries
- Contact forms
- Resume/CV sections

### Forum
- Topics, Posts, Replies
- User reputation system
- Moderation tools
- Search functionality

### Wiki
- Pages, Categories, Revisions
- Markdown support
- Version control
- Collaborative editing

### E-Learning
- Courses, Lessons, Quizzes
- Student progress tracking
- Video integration
- Certificates

### Social
- User profiles, Posts, Follows
- Activity feeds
- Messaging system
- Notifications

### CRM
- Contacts, Deals, Tasks
- Pipeline management
- Email integration
- Analytics dashboard

### Shop
- Products, Orders, Cart
- Payment processing
- Inventory management
- Customer reviews

## 🔧 Configuration

### Authentication Options
- `jwt` - JWT-based authentication with djangorestframework-simplejwt
- `session` - Traditional Django session authentication
- `allauth` - Social authentication with django-allauth

### UI Frameworks
- `tailwind` - Tailwind CSS with Alpine.js
- `bootstrap` - Bootstrap 5 with jQuery
- `none` - No UI framework (API-only)

## 🐳 Docker Support

CoreX projects come with Docker configuration out of the box:

```bash
# Run with Docker
corex runserver --docker

# Build and run production
docker-compose -f docker-compose.prod.yml up --build
```

## 🧪 Testing

```bash
# Run all tests
corex test

# Run specific app tests
corex test blog

# Run with coverage
corex test --coverage
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Rails generators and Laravel Artisan
- Built with modern Python tooling (Poetry, Click, Rich)
- Designed for Django developers by Django developers
