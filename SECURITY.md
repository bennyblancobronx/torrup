# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability in Torrup, please report it responsibly.

### Do NOT

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it's fixed

### Do

1. Email security@torrup-project.dev or open a [private vulnerability report](https://github.com/bennyblancobronx/torrup/security/advisories/new)
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit in the fix announcement (if desired)

## Security Configuration

### Required

| Setting | Purpose |
|---------|---------|
| `SECRET_KEY` | Flask session encryption. App will not start without this. |

Generate with:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Optional Authentication

For local/home network use, authentication is optional. If exposing Torrup outside localhost, enable basic auth:

```bash
export TORRUP_AUTH_USER=admin
export TORRUP_AUTH_PASS=your_strong_password
```

When both variables are set, all routes require authentication. When unset, no auth is enforced.

### Built-in Protections

Torrup includes these security measures:

- **CSRF protection** - All state-changing requests require a valid CSRF token
- **Rate limiting** - Request rate limits to prevent abuse
- **Security headers** - X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
- **Input validation** - Release names, categories, tags are validated and sanitized
- **Path traversal prevention** - File browser is restricted to configured media roots
- **Error sanitization** - Internal paths and secrets are stripped from error messages
- **No debug mode** - Production-safe defaults

## Security Best Practices for Users

1. **Never commit credentials**
   - Use environment variables for API keys
   - Keep `.env` files out of version control

2. **Use HTTPS**
   - Use a reverse proxy (nginx, traefik) for HTTPS
   - Required if exposing to internet

3. **Keep dependencies updated**
   - Regularly update Python packages
   - Monitor for security advisories

4. **Secure your deployment**
   - Use strong passwords for TORRUP_AUTH_PASS
   - Limit network exposure (bind to localhost or use firewall)
   - Keep media volumes read-only where possible
