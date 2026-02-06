# Contributing to Torrup

Thank you for your interest in contributing to Torrup (Torrent Upload Tool).

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Keep functions focused and under 50 lines when possible
- Add docstrings to public functions

### File Organization

- Source code goes in `/src`
- Tests go in `/tests`
- Documentation goes in `/docs`
- Utility scripts go in `/scripts`

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep the first line under 72 characters
- Reference issues when applicable: `Fix #123`

Example:
```
Add torrent validation before upload

- Validate file exists and is readable
- Check file size limits
- Verify torrent metadata
```

### Testing

- Write tests for new functionality
- Run tests before submitting:
  ```bash
  pytest tests/
  ```
- Ensure all tests pass

### Pull Requests

1. Update documentation if needed
2. Add tests for new features
3. Ensure CI passes
4. Fill out the PR template completely
5. Request review from maintainers

## Reporting Issues

- Use the issue templates provided
- Include steps to reproduce bugs
- Provide environment details (OS, Python version)
- Include relevant logs or error messages

## Security

If you discover a security vulnerability, please see [SECURITY.md](SECURITY.md) for reporting instructions. Do not open a public issue for security vulnerabilities.

## Questions

Open a discussion or issue if you have questions about contributing.
