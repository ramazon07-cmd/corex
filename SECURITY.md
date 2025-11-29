# CoreX Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in CoreX, please follow these steps:

1. **Do not** create a public issue on GitHub
2. Send an email to security@corex.io with the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes

We will respond within 48 hours and work with you to resolve the issue.

## Security Best Practices

### Input Sanitization
- All user inputs are sanitized before processing
- Template generation uses parameterized queries where applicable
- File paths are validated to prevent directory traversal attacks

### Authentication & Authorization
- WebSocket connections require token-based authentication
- Tokens are generated using cryptographically secure random generators
- All API endpoints validate user permissions

### Data Protection
- Sensitive data is encrypted at rest
- Communications between CLI and GUI use secure WebSocket connections
- Environment variables are used for sensitive configuration

### Dependency Management
- Regular security audits using bandit and safety
- Dependabot configured for automatic dependency updates
- Third-party packages are reviewed for security vulnerabilities

## Automated Security Scans

CoreX uses the following tools for automated security scanning:

1. **Bandit** - Python security linter
2. **Safety** - Dependency vulnerability scanner
3. **Snyk** - Continuous security monitoring
4. **GitHub Security** - Code scanning and secret detection

## Compliance

CoreX follows these security standards:
- OWASP Top 10
- NIST Cybersecurity Framework
- ISO 27001 (where applicable)

## Template Security

Industry templates include built-in security features:
- CSRF protection
- XSS prevention
- SQL injection prevention
- Secure authentication patterns
- Role-based access control

## GUI Security

The CoreX GUI implements:
- Secure WebSocket communication
- Token-based authentication
- Input validation
- CORS protection
- Content Security Policy (CSP)