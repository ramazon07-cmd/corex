# Template Guide for CoreX

This guide explains best practices for creating and maintaining templates used by CoreX generators.

## Core Principles

- Use Jinja2 for templating. Keep placeholders explicit and documented.
- Avoid using expressions that conflict with Django template tags. When embedding Django templates inside Jinja2 templates, use raw blocks or escape sequences.
- Provide sane defaults and ensure production-safe defaults (e.g. DEBUG=False in .env.example).
- Always include an `.env.example` with warnings and non-sensitive placeholders.
- Add a unit test or smoke test in the `tests/` folder that verifies the template renders without unresolved placeholders.
- Use `{{ project_name }}`, `{{ auth }}`, `{{ ui }}`, `{{ database }}`, and `{{ python_version }}` as standard variables.

## Validator

- CoreX provides a template validator function `scan_project_for_unresolved_placeholders` in `corex.utils`.
- Run the validator after generating a project and fail CI if placeholders are found.

## Industry-Specific Template Guidelines

### Education Templates

Education templates should include comprehensive models for academic institutions:

1. **Student Management**
   - Student profiles with personal and academic information
   - Enrollment tracking across courses and semesters
   - Grade management and academic progress tracking
   - Attendance records

2. **Course Management**
   - Course catalogs with detailed descriptions
   - Instructor assignments and scheduling
   - Semester/term management
   - Prerequisites and course dependencies

3. **Assessment Tools**
   - Assignment creation and distribution
   - Submission management
   - Grading systems
   - Feedback mechanisms

4. **Communication Features**
   - Announcements and notifications
   - Resource sharing
   - Discussion forums

### Fintech Templates

Fintech templates should provide robust financial management capabilities:

1. **Account Management**
   - Multiple account types (checking, savings, credit, investment)
   - Balance tracking and transaction history
   - Currency support

2. **Transaction Processing**
   - Income and expense tracking
   - Transfer management
   - Recurring transactions
   - Category-based organization

3. **Financial Planning**
   - Budget creation and monitoring
   - Goal tracking
   - Investment portfolio management
   - Invoice generation

4. **Reporting Features**
   - Financial summaries
   - Spending analysis
   - Trend visualization

### Healthcare Templates

Healthcare templates should prioritize patient care and medical record management:

1. **Patient Management**
   - Comprehensive patient profiles
   - Medical history tracking
   - Emergency contact information
   - Insurance details

2. **Provider Management**
   - Healthcare professional profiles
   - Specialty and department assignments
   - Availability scheduling

3. **Appointment Scheduling**
   - Booking system
   - Calendar integration
   - Reminders and notifications

4. **Medical Records**
   - Clinical notes and observations
   - Prescription management
   - Test results tracking
   - Treatment plans

5. **Compliance Features**
   - HIPAA compliance considerations
   - Audit trails
   - Secure data handling

## Template Structure

### Project Templates

Project templates should be organized in the `corex/templates/projects/` directory:

```
projects/
├── manage.py.j2
├── settings.py.j2
├── urls.py.j2
├── wsgi.py.j2
├── asgi.py.j2
├── pyproject.toml.j2
├── requirements.txt.j2
├── README.md.j2
├── .env.j2
├── .env.example.j2
├── base.html.j2
├── docker/
│   ├── Dockerfile.j2
│   ├── docker-compose.yml.j2
│   └── docker-compose.prod.yml.j2
└── ui/
    ├── tailwind/
    │   ├── tailwind.config.js.j2
    │   ├── package.json.j2
    │   └── input.css.j2
    └── bootstrap/
        ├── package.json.j2
        └── style.css.j2
```

### App Templates

App templates should be organized in the `corex/templates/apps/` directory:

```
apps/
├── apps.py.j2
├── models.py.j2
├── views.py.j2
├── urls.py.j2
├── admin.py.j2
├── tests/
│   ├── test_models.py.j2
│   └── test_views.py.j2
├── templates/
│   ├── list.html.j2
│   ├── detail.html.j2
│   └── form.html.j2
├── api/
│   ├── serializers.py.j2
│   ├── views.py.j2
│   └── urls.py.j2
├── management/
│   └── seed.py.j2
└── types/
    ├── blog.py.j2
    ├── shop.py.j2
    ├── wiki.py.j2
    ├── crm.py.j2
    ├── social.py.j2
    ├── forum.py.j2
    ├── portfolio.py.j2
    ├── elearn.py.j2
    ├── education.py.j2
    ├── fintech.py.j2
    └── healthcare.py.j2
```

## Best Practices

### Model Design

1. **Use descriptive field names** that clearly indicate their purpose
2. **Include help_text** for complex fields
3. **Add verbose_name** for better admin interface
4. **Use appropriate field types** (CharField, TextField, DateTimeField, etc.)
5. **Define __str__ methods** for all models
6. **Add get_absolute_url methods** for detail views
7. **Include Meta classes** with ordering and other options

### View Design

1. **Use class-based views** for consistency
2. **Implement proper permissions** and authentication
3. **Add form validation** and error handling
4. **Include pagination** for list views
5. **Provide search functionality** where appropriate

### Template Design

1. **Use template inheritance** with base templates
2. **Implement responsive design** principles
3. **Include proper meta tags** for SEO
4. **Add accessibility features** (ARIA labels, semantic HTML)
5. **Use consistent styling** with the selected UI framework

### API Design

1. **Follow REST principles** for endpoint design
2. **Include proper serialization** of related objects
3. **Implement pagination** for list endpoints
4. **Add filtering and search** capabilities
5. **Include proper error responses** with status codes

## Testing Templates

Each template should include appropriate tests:

1. **Model Tests**
   - Field validation
   - Method functionality
   - Relationship integrity

2. **View Tests**
   - Response codes
   - Template rendering
   - Form handling

3. **API Tests**
   - Endpoint accessibility
   - Data serialization
   - Authentication requirements

4. **Integration Tests**
   - User workflows
   - Data flow between components

## Documentation

Templates should include comprehensive documentation:

1. **README.md** with setup instructions
2. **Inline comments** explaining complex logic
3. **Code examples** for common use cases
4. **API documentation** for endpoints
5. **Configuration guides** for deployment

## Version Control

1. **Use semantic versioning** for template updates
2. **Maintain changelogs** for significant changes
3. **Tag releases** for easy rollback
4. **Document breaking changes** clearly
5. **Provide migration guides** when possible

## Security Considerations

1. **Validate all user input** to prevent injection attacks
2. **Implement proper authentication** and authorization
3. **Use Django's built-in security features**
4. **Sanitize output** to prevent XSS attacks
5. **Protect sensitive data** with encryption where necessary
6. **Regularly update dependencies** to patch vulnerabilities

By following these guidelines, you can create robust, maintainable templates that provide maximum value to CoreX users while ensuring security and best practices.