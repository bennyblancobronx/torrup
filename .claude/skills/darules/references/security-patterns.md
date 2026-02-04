# Security Patterns Reference

Patterns used by the security scan to detect secrets and sensitive data.

## Blocking Patterns (Never Commit)

### File Types

| Pattern | Description |
|---------|-------------|
| `.env`, `.env.*` | Environment files (except .env.example) |
| `*.pem` | PEM certificate/key files |
| `*.key` | Private key files |
| `id_rsa`, `id_rsa.*` | SSH private keys |
| `credentials.json` | Google/AWS credential files |
| `serviceAccount.json` | GCP service account keys |

### Content Patterns

| Pattern | Example Match |
|---------|---------------|
| `api_key = "..."` | `API_KEY = "sk-abc123..."` |
| `secret_key: "..."` | `SECRET_KEY: "super_secret_value"` |
| `password = "..."` | `password = "hunter2"` |
| `private_key: "..."` | `PRIVATE_KEY: "-----BEGIN RSA..."` |
| `bearer <token>` | `Authorization: Bearer eyJhbGc...` |
| `://user:pass@host` | `postgres://admin:secret@db.example.com` |

### Regex Patterns Used

```regex
# API keys and secrets with values
(api[_-]?key|secret[_-]?key|password|private[_-]?key)\s*[:=]\s*["'][^"']{8,}

# Bearer tokens
bearer\s+[a-zA-Z0-9_-]{20,}

# Connection strings with credentials
://[^:]+:[^@]+@
```

## Warning Patterns (Review Before Commit)

### Debug Statements

| Pattern | Found In |
|---------|----------|
| `console.log(...)` | JavaScript/TypeScript (non-test files) |
| `console.debug(...)` | JavaScript/TypeScript (non-test files) |
| `print(...)` | Python (non-test files) |
| `debugger` | JavaScript/TypeScript |

### Test File Issues

| Pattern | Concern |
|---------|---------|
| `.only()` | Test exclusivity - other tests won't run |
| `.skip()` | Skipped test - may hide failures |

### Incomplete Work

| Pattern | Concern |
|---------|---------|
| `TODO` | Incomplete implementation |
| `FIXME` | Known issue not resolved |

## Files to Never Stage

These are automatically excluded regardless of content:

```
# Dependencies
node_modules/
__pycache__/
.venv/
vendor/
bower_components/

# Build outputs
dist/
build/
out/
*.o
*.pyc
*.pyo
*.class

# IDE files
.idea/
.vscode/settings.json
.vscode/launch.json
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Logs
*.log
npm-debug.log*
yarn-error.log*

# Coverage
coverage/
.nyc_output/
htmlcov/
```

## False Positive Handling

Some patterns may trigger false positives. Common exceptions:

| Pattern | When It's OK |
|---------|--------------|
| `password = "..."` | In test fixtures with dummy data |
| `api_key = "..."` | In .env.example with placeholder values |
| `console.log` | In CLI tools where it's the output mechanism |
| `TODO` | In documentation describing future work |

When a false positive is detected, the user can:
1. Acknowledge the warning and proceed
2. Add a `# nosec` or `// nosec` comment to suppress (not implemented yet)
3. Move test data to dedicated fixture files

## Best Practices

1. **Use environment variables** for all secrets
2. **Use .env.example** to document required variables (with dummy values)
3. **Add .env to .gitignore** in every project
4. **Use secret managers** (AWS Secrets Manager, HashiCorp Vault) for production
5. **Rotate secrets immediately** if accidentally committed
6. **Check git history** - removing a file doesn't remove it from history
