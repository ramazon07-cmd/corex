# CoreX Runbook

## Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git
- Docker (optional but recommended)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/corex.git
cd corex

# Run the bootstrap script for your OS
# On macOS/Linux:
./scripts/bootstrap.sh

# On Windows:
.\scripts\bootstrap.ps1
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv corex-env
source corex-env/bin/activate  # On Windows: corex-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install CoreX in development mode
pip install -e .

# Install GUI dependencies
cd gui/corex-gui
npm install
cd ../..
```

## Running the Application

### CLI Usage

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

### GUI Usage

```bash
# Start the CoreX agent (in one terminal)
python -m corex.agent.server

# Start the GUI (in another terminal)
cd gui/corex-gui
npm run dev
```

Visit `http://localhost:3000` to access the GUI.

## Template Development

### Creating a New Industry Template

1. Create a new directory in `corex/templates/industry/`
2. Add required files:
   - `schema.json` - Template metadata
   - `models.py` - Domain models
   - `generators.py` - Template generation logic
3. Add tests in `tests/` directory
4. Validate with the template validator

### Template Validation

```bash
# Validate a template
python -m corex.template_validator corex/templates/industry/ecommerce
```

### Running Template Tests

```bash
# Run industry template tests
python -m pytest test_industry_templates.py -v
```

## Cross-Platform Development

### Testing on Different Platforms

The CI pipeline automatically tests on:
- Ubuntu (latest)
- Windows (latest)
- macOS (latest)

For local cross-platform testing, use Docker:

```bash
# Test in Ubuntu container
docker run -it -v $(pwd):/app python:3.10 bash
cd /app
# Run tests as described above
```

## CI/CD Pipeline

### GitHub Actions Workflow

The pipeline runs on every push and pull request to the main branch:

1. **Test Job**:
   - Runs on Ubuntu, Windows, and macOS
   - Tests multiple Python versions (3.8, 3.9, 3.10)
   - Template validation
   - Linting with flake8
   - Unit tests with pytest
   - Cross-platform smoke tests

2. **Docker Job**:
   - Builds and pushes Docker images
   - Runs only on main branch

3. **Security Job**:
   - Runs security scans with Bandit
   - Checks dependencies with Safety

### Running CI Locally

```bash
# Run template validation
python -m corex.template_validator corex/templates/industry/ecommerce
python -m corex.template_validator corex/templates/industry/legal
python -m corex.template_validator corex/templates/industry/realestate
python -m corex.template_validator corex/templates/industry/healthcare
python -m corex.template_validator corex/templates/industry/fintech

# Run linting
pip install flake8
flake8 corex --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 corex --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests
pip install pytest pytest-cov
pytest --cov=corex --cov-report=xml
```

## AST Refactoring

### Refactoring for Django Version Changes

```bash
# Refactor code for Django 3 to 4 compatibility
python -m corex.ast_refactor myproject/ --target django_3_to_4
```

### Adding New Refactor Rules

1. Update the rules in `corex/ast_refactor.py`
2. Add test cases in `test_industry_templates.py`
3. Validate with existing templates

## Environment Checking

### Running Environment Checks

```bash
# Check environment health
python -m corex.env_checker
```

## Security

### Running Security Scans

```bash
# Install security tools
pip install bandit safety

# Run bandit security scan
bandit -r corex -f json -o bandit-report.json

# Check for vulnerable dependencies
safety check
```

## Deployment

### Building Docker Images

```bash
# Build CoreX Docker image
docker build -t corex/corex .

# Run CoreX container
docker run -p 8000:8000 corex/corex
```

### Publishing to Docker Hub

The CI pipeline automatically publishes to Docker Hub on pushes to the main branch.

## Troubleshooting

### Common Issues

1. **WebSocket connection fails**:
   - Ensure the CoreX agent is running
   - Check that the authentication token is valid
   - Verify firewall settings

2. **Template validation fails**:
   - Check that all required files exist
   - Validate JSON/YAML syntax
   - Ensure models are properly defined

3. **Cross-platform issues**:
   - Use Docker for consistent environments
   - Check file permissions (especially on Windows)
   - Verify line endings (CRLF vs LF)

### Getting Help

1. Check the documentation in `usages/`
2. Open an issue on GitHub
3. Contact the maintainers

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests
5. Run all tests
6. Commit and push
7. Create a Pull Request

### Code Standards

- Follow PEP 8 for Python code
- Use TypeScript for GUI components
- Write comprehensive tests
- Document new features
- Update README.md as needed

### Testing Requirements

- Unit tests for all new functionality
- Integration tests for key workflows
- Cross-platform compatibility verification
- Security scanning for new dependencies