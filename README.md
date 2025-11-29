# CoreX - AI-Assisted Django Scaffolding Framework

[![CI](https://github.com/yourusername/corex/workflows/CoreX%20CI/badge.svg)](https://github.com/yourusername/corex/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.2%2B-blue.svg)](https://www.djangoproject.com/)

CoreX is a comprehensive Django scaffolding framework that accelerates development with AI-assisted features, industry-specific templates, and seamless CLI↔GUI integration.

## Features

### 🏭 Industry Templates
Specialized templates for 5 key industries:
- **E-commerce**: Online stores and marketplaces
- **Legal Services**: Law firms and legal tech
- **Real Estate**: Property listings and management
- **Healthcare**: Clinics and medical systems
- **Financial Technology**: Fintech and payment systems

### 🤖 AI-Assisted Development
- Intelligent template selection based on project requirements
- Automated code refactoring for Django version upgrades
- Smart dependency management
- Predictive suggestions in GUI

### 🔗 CLI↔GUI Synchronization
- Real-time bidirectional communication
- WebSocket-based protocol with JSON-RPC
- Live progress tracking
- Secure authentication

### 🌍 Cross-Platform Compatibility
- Works on Windows, macOS, and Linux
- Docker-first development approach
- Native bootstrappers for each platform
- Consistent behavior across environments

### 🔄 Django Version Compatibility
- Automatic refactoring for version upgrades
- Compatibility matrix for all templates
- Nightly compatibility testing
- Safe AST-based transforms

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/corex.git
cd corex

# Install dependencies
pip install -r requirements.txt

# Install CoreX
pip install -e .
```

### Using the CLI

```bash
# Create a new project with an industry template
corex new myproject --template ecommerce --auth jwt --ui tailwind --database postgres

# Generate an app with industry template
corex app myapp --type legal --auth session --ui bootstrap

# Run the development server
corex runserver

# Run tests
corex test
```

### Using the GUI

```bash
# Start the CoreX agent
python -m corex.agent.server

# In another terminal, start the GUI
cd gui/corex-gui
npm run dev
```

Visit `http://localhost:3000` to access the GUI.

## Industry Templates

Each industry template provides domain-specific models, views, and features:

### E-commerce Template
```bash
corex new mystore --template ecommerce
```
Features:
- Product catalog with images
- Shopping cart and checkout
- Order management
- Payment integration
- Inventory tracking

### Legal Services Template
```bash
corex new mylawfirm --template legal
```
Features:
- Client management
- Case tracking
- Document management
- Time billing
- Court calendar

### Real Estate Template
```bash
corex new myrealestate --template realestate
```
Features:
- Property listings
- Agent profiles
- Client management
- Transaction tracking
- Appointment scheduling

### Healthcare Template
```bash
corex new myclinic --template healthcare
```
Features:
- Patient records
- Appointment scheduling
- Medical history
- Prescription management
- Billing and insurance

### Financial Technology Template
```bash
corex new myfintech --template fintech
```
Features:
- Account management
- Transaction processing
- Payment integration
- Budgeting tools
- Investment tracking

## Template Validation

CoreX includes a comprehensive template validator:

```bash
python -m corex.template_validator corex/templates/industry/ecommerce
```

## AST Refactoring

Automatically refactor code for Django version compatibility:

```bash
python -m corex.ast_refactor myproject/ --target django_3_to_4
```

## Cross-Platform Bootstrap

Platform-specific bootstrap scripts ensure consistent setup:

### macOS/Linux
```bash
./scripts/bootstrap.sh
```

### Windows
```powershell
.\scripts\bootstrap.ps1
```

## Development Workflow

1. **Create Project**: Use CLI or GUI to generate a new project
2. **Customize**: Modify generated code to fit requirements
3. **Test**: Run unit and integration tests
4. **Deploy**: Use built-in deployment commands

## CI/CD Integration

CoreX includes GitHub Actions workflows for:
- Cross-platform testing
- Security scanning
- Template validation
- Docker image building

## Security

CoreX follows security best practices:
- Input sanitization
- Secure authentication
- Data encryption
- Regular security audits

See [SECURITY.md](SECURITY.md) for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

CoreX is released under the MIT License. See [LICENSE](LICENSE) for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.