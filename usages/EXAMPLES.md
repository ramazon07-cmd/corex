# CoreX Examples

This document provides practical examples of how to use CoreX's new features.

## Industry-Specific Templates

### Education Management System

Create a comprehensive education management system:

```bash
# Create a new project with JWT authentication and Tailwind CSS
corex new lms --auth=jwt --ui=tailwind --database=postgres --docker --api

# Navigate to the project directory
cd lms

# Generate an education app with all models and demo data
corex app education --type=education --seed --api

# Run migrations
corex migrate

# Start the development server
corex runserver
```

This creates a complete education management system with:
- Student and instructor management
- Course catalog and enrollment
- Grade tracking and attendance
- Assignments and submissions
- Announcements and resources

### Fintech Application

Create a financial management application:

```bash
# Create a new fintech project
corex new fintech_app --auth=session --ui=tailwind --database=postgres --docker

# Navigate to the project directory
cd fintech_app

# Generate a fintech app with all models
corex app finance --type=fintech --api --seed

# Run migrations
corex migrate

# Start the development server
corex runserver
```

This creates a complete financial management system with:
- Account and transaction management
- Budgeting and financial tracking
- Invoicing and billing
- Investment portfolio tracking
- Financial goal planning

### Healthcare Management System

Create a healthcare management application:

```bash
# Create a new healthcare project with JWT authentication
corex new clinic --auth=jwt --ui=tailwind --database=postgres --docker --api

# Navigate to the project directory
cd clinic

# Generate a healthcare app with all models
corex app patients --type=healthcare --api --seed

# Run migrations
corex migrate

# Start the development server
corex runserver
```

This creates a complete healthcare management system with:
- Patient and provider management
- Appointment scheduling
- Medical records and prescriptions
- Billing and insurance
- Vaccination tracking

## GUI Usage Examples

### Creating a Project with the GUI

1. Start the GUI:
   ```bash
   cd gui/corex-gui
   npm install
   npm run dev
   ```

2. Open your browser to `http://localhost:3000`

3. Select "New Project" tab

4. Configure your project:
   - Project Name: `my_blog`
   - Authentication: `Session (Traditional)`
   - UI Framework: `Tailwind CSS`
   - Database: `SQLite (Development)`
   - Check "Include Docker Configuration"
   - Check "Include Django REST Framework"

5. Click "Create Project"

6. The GUI will execute the command and show the results:
   ```
   corex new my_blog --auth=session --ui=tailwind --database=sqlite --docker --api
   ```

### Creating an App with the GUI

1. Ensure you're in a Django project directory

2. In the GUI, select "New App" tab

3. Configure your app:
   - App Name: `blog`
   - App Type: `Blog (Posts, Comments)`
   - Authentication Override: `Use Project Default`
   - UI Framework Override: `Use Project Default`
   - Check "Generate Demo Data"
   - Check "Include API Endpoints"

4. Click "Create App"

5. The GUI will execute the command and show the results:
   ```
   corex app blog --type=blog --seed --api
   ```

## Advanced Usage Examples

### Multi-App Platform

Create a platform with multiple specialized apps:

```bash
# Create a platform project
corex new platform --auth=allauth --ui=tailwind --database=postgres --docker --api

# Navigate to the project directory
cd platform

# Add a blog app
corex app blog --type=blog --api --seed

# Add an e-commerce app
corex app store --type=shop --api --seed

# Add a social network app
corex app community --type=social --api --seed

# Add a healthcare app
corex app patients --type=healthcare --api --seed

# Add a fintech app
corex app finance --type=fintech --api --seed

# Run migrations
corex migrate

# Create a superuser
corex createsuperuser

# Start the development server
corex runserver
```

### CI/CD Integration

Set up continuous integration and deployment:

```bash
# Initialize GitHub Actions
corex ci --github --docker

# The above command creates:
# - .github/workflows/ci.yml with testing, linting, and deployment
# - Docker configuration for containerized deployment
```

### Service Integration

Add external services to your project:

```bash
# Add Redis for caching and sessions
corex integrate redis

# Add Celery for background tasks
corex integrate celery

# Add Stripe for payment processing
corex integrate stripe

# Add AWS S3 for file storage
corex integrate s3
```

### Deployment Examples

Deploy to various cloud platforms:

```bash
# Deploy to Vercel
corex deploy --platform=vercel --domain=myapp.example.com

# Deploy to Railway with auto-provisioned database
corex deploy --platform=railway --auto-db --region=us-west

# Deploy to Heroku
corex deploy --platform=heroku --env-file=.env.prod
```

## Testing and Quality Assurance

Run comprehensive tests for your applications:

```bash
# Run all tests
corex test

# Run tests with coverage
corex test --coverage

# Run tests in parallel for faster execution
corex test --parallel

# Run tests for a specific app
corex test blog
```

## Health Checks and Maintenance

Monitor and maintain your project:

```bash
# Run a comprehensive health check
corex doctor

# Auto-fix common issues
corex doctor --fix

# Generate demo data for testing
corex seed --count=50

# Generate demo data for a specific app
corex seed --app=blog --count=20
```

These examples demonstrate the power and flexibility of CoreX for creating Django applications across various industries, with both CLI and GUI interfaces.