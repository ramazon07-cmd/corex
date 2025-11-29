# CoreX Industry Templates

CoreX now includes specialized templates for 5 key industries, each with domain-specific models, features, and best practices.

## Available Industry Templates

### 1. E-commerce (`ecommerce`)
Template for online stores, marketplaces, and e-commerce platforms.

**Key Features:**
- Product catalog with categories and images
- Shopping cart and checkout workflow
- Order management and tracking
- Customer accounts and profiles
- Payment integration (Stripe-ready)
- Inventory management
- Product reviews and ratings

**Modules:**
- Products
- Orders
- Payments
- Inventory
- Reviews
- Coupons

### 2. Legal Services (`legal`)
Template for law firms, legal consultancies, and legal tech applications.

**Key Features:**
- Client management
- Case/matter tracking
- Document management
- Time tracking and billing
- Court calendar integration
- Attorney profiles

**Modules:**
- Clients
- Cases
- Documents
- Billing
- Calendar
- Matters

### 3. Real Estate (`realestate`)
Template for real estate agencies, property management, and listings.

**Key Features:**
- Property listings with photos
- Agent profiles and specialties
- Client management
- Transaction tracking
- Appointment scheduling
- Property search and filtering

**Modules:**
- Properties
- Listings
- Agents
- Transactions
- Clients
- Calendar

### 4. Healthcare (`healthcare`)
Template for clinics, hospitals, and healthcare management systems.

**Key Features:**
- Patient records management
- Appointment scheduling
- Medical records and history
- Prescription management
- Billing and insurance
- Medical staff profiles

**Modules:**
- Patients
- Appointments
- Medical Records
- Billing
- Staff
- Inventory

### 5. Financial Technology (`fintech`)
Template for fintech startups, payment processors, and financial services.

**Key Features:**
- Account management
- Transaction processing
- Payment integration
- Budgeting tools
- Investment tracking
- Compliance reporting

**Modules:**
- Accounts
- Transactions
- Payments
- Compliance
- Analytics
- Investments

## Using Industry Templates

### Via CLI
```bash
# Create a new project with an industry template
corex new myproject --template ecommerce --auth jwt --ui tailwind --database postgres

# Generate an app with industry template
corex app myapp --type legal --auth session --ui bootstrap
```

### Via GUI
1. Open the CoreX GUI
2. Select "New Project"
3. Choose your industry template from the dropdown
4. Configure authentication, UI, and database options
5. Click "Create Project"

## Template Customization

Each industry template can be customized:

### Module Selection
```bash
# Generate only specific modules
corex new myproject --template ecommerce --modules products,orders,payments
```

### Configuration Options
Each template includes a `schema.json` file that defines:
- Required modules
- Dependencies
- Configuration options

## Template Validation

CoreX includes a template validator to ensure templates meet quality standards:

```bash
# Validate a template
python -m corex.template_validator corex/templates/industry/ecommerce
```

The validator checks:
- Directory structure
- Required files
- Model definitions
- Static analysis
- Compatibility

## Cross-Platform Compatibility

All industry templates are tested on:
- Windows 10/11
- macOS 10.15+
- Ubuntu 20.04+

## Django Version Compatibility

Templates are compatible with:
- Django 3.2 LTS
- Django 4.2 LTS
- Django 5.x (latest)

## Extending Templates

To create a custom industry template:

1. Copy an existing template as a base
2. Modify the `schema.json` file
3. Update the models in `models.py`
4. Create custom views and templates
5. Add tests in the `tests/` directory
6. Validate with the template validator

## Contributing Templates

To contribute a new industry template:

1. Fork the CoreX repository
2. Create a new directory in `corex/templates/industry/`
3. Follow the existing template structure
4. Include all required files
5. Add comprehensive tests
6. Validate with the template validator
7. Submit a pull request

## Template Architecture

Each industry template follows a modular architecture:

```
industry/
├── template_name/
│   ├── schema.json          # Template metadata
│   ├── models.py           # Domain models
│   ├── generators.py       # Template generation logic
│   ├── views.py.j2         # Jinja2 view templates
│   ├── urls.py.j2          # Jinja2 URL configuration
│   ├── templates/          # HTML templates
│   │   ├── base.html.j2
│   │   └── *.html.j2
│   ├── static/             # Static assets
│   │   ├── css/
│   │   └── js/
│   ├── tests/              # Unit tests
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   └── test_forms.py
│   └── fixtures/           # Sample data
│       ├── *.json
```

## Template Complexity Management

CoreX uses several strategies to manage template complexity:

1. **Composable Micro-Templates**: Each template is broken into small, focused modules
2. **Config-Driven Variability**: Templates can be configured for different feature sets
3. **Sample Datasets**: Each template includes fixtures for rapid demos
4. **Template Orchestrator**: Assembles modules based on user selection

## Security Considerations

Industry templates include built-in security best practices:
- CSRF protection
- XSS prevention
- SQL injection prevention
- Secure authentication patterns
- Role-based access control
- Data encryption for sensitive fields

## Performance Optimization

Templates are optimized for:
- Database query efficiency
- Caching strategies
- Static asset optimization
- Responsive design
- Mobile-first approach

## Testing

Each template includes:
- Unit tests for models and views
- Integration tests for key workflows
- API tests for REST endpoints
- Browser compatibility tests
- Performance benchmarks

Run template tests with:
```bash
cd myproject
python manage.py test
```