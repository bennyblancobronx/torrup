# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | Yes                |

## Reporting a Vulnerability

If you discover a security vulnerability in TLT, please report it responsibly.

### Do NOT

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it's fixed

### Do

1. Email the maintainers directly with details
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- Acknowledgment within 48 hours
- Regular updates on progress
- Credit in the fix announcement (if desired)

## Security Best Practices for Users

1. **Never commit credentials**
   - Use environment variables for API keys
   - Keep `.env` files out of version control

2. **Use HTTPS**
   - Always use HTTPS in production
   - Verify SSL certificates

3. **Keep dependencies updated**
   - Regularly update Python packages
   - Monitor for security advisories

4. **Secure your deployment**
   - Use strong passwords
   - Limit network exposure
   - Enable logging and monitoring
