# Docker Repository Best Practices

> Researched: 2026-02-03 | Sources: 6 fetched, 6 cited

## Overview

A well-structured Docker repository contains three core files: a Dockerfile, a .dockerignore, and a docker-compose.yml (or compose.yaml). These files should be kept at the project root for discoverability and version controlled alongside application code. The goal is reproducible, secure, minimal images that can be built and run consistently across environments.

Modern Docker best practices emphasize multi-stage builds, non-root users, health checks, and proper secret management. The `docker init` command can scaffold these files automatically, but understanding what each should contain ensures production-grade results.

## Core Files

### 1. Dockerfile

The Dockerfile defines how to build your container image. Required/recommended elements:

| Element | Purpose | Required |
|---------|---------|----------|
| `FROM` | Base image (use official, pin version) | Yes |
| `WORKDIR` | Set working directory (absolute path) | Yes |
| `COPY` | Add application files | Yes |
| `RUN` | Install dependencies, create users | Yes |
| `USER` | Run as non-root (UID > 10000 ideal) | Recommended |
| `EXPOSE` | Declare listening ports | Recommended |
| `HEALTHCHECK` | Container health monitoring | Recommended |
| `CMD`/`ENTRYPOINT` | Default command | Yes |
| `LABEL` | Metadata for organization | Optional |
| `ENV` | Environment defaults | Optional |

**Key rules:**
- Combine `apt-get update && apt-get install` in one RUN to avoid cache issues
- Clean up package manager caches (`rm -rf /var/lib/apt/lists/*`)
- Pin base image versions (avoid `latest`)
- Use multi-stage builds for compiled languages
- Order instructions from least to most frequently changing (for cache efficiency)

### 2. .dockerignore

Excludes files from the build context. Critical for:
- Faster builds (less data transferred to daemon)
- Smaller images
- Security (no secrets in image)
- Better cache utilization

**Must exclude:**
```
.git
node_modules/
__pycache__/
*.pyc
.env
.env.*
*.log
.aws/
*.db
```

**Should exclude:**
```
docs/
tests/
*.md
.vscode/
.idea/
.DS_Store
docker-compose*.yml
```

### 3. docker-compose.yml (or compose.yaml)

Defines multi-container applications. Modern files omit the `version:` field.

**Required elements:**
- `services:` block with service definitions
- `image:` or `build:` for each service
- `ports:` for exposed services

**Recommended elements:**
- `healthcheck:` for production reliability
- `restart:` policy (unless-stopped or always)
- `volumes:` for persistent data
- `environment:` or `env_file:` for configuration
- Resource limits (`deploy.resources`) for production

**File structure for environments:**
- `docker-compose.yml` - base configuration
- `docker-compose.override.yml` - dev overrides (auto-loaded)
- `docker-compose.prod.yml` - production overrides

## Best Practices Summary

1. **Pin versions** - Never use `latest` tag; pin to specific versions or SHA digests
2. **Non-root user** - Create and switch to unprivileged user (UID > 10000)
3. **Health checks** - Define in both Dockerfile and compose file
4. **Minimal images** - Use slim/alpine bases, remove unnecessary packages
5. **Multi-stage builds** - Separate build and runtime stages
6. **Secrets management** - Use environment variables, never hardcode
7. **Layer optimization** - Order commands by change frequency
8. **Clean up** - Remove package caches and temporary files
9. **One concern per container** - Separate services, use networks
10. **.dockerignore** - Always exclude .git, secrets, and dev artifacts

## Common Pitfalls

- Using `apt-get update` alone (causes stale package lists)
- Running as root (security risk)
- Not using .dockerignore (slow builds, large images, secret leaks)
- Hardcoding secrets in Dockerfile or compose
- Missing health checks (orchestrators can't detect failures)
- Using `latest` tag (non-reproducible builds)

---

## Audit: Current Project

### Dockerfile Analysis

| Criteria | Status | Notes |
|----------|--------|-------|
| Official base image | PASS | `python:3.11-slim` |
| Version pinned | PASS | `3.11-slim` specific |
| Combined apt-get | PASS | update && install in one RUN |
| Cache cleanup | PASS | `rm -rf /var/lib/apt/lists/*` |
| Non-root user | PASS | `appuser` created and used |
| WORKDIR set | PASS | `/app` |
| HEALTHCHECK | PASS | curl-based, 30s interval |
| EXPOSE | PASS | 5001 |
| CMD present | PASS | gunicorn with exec form |
| Multi-stage build | N/A | Not needed for Python |
| LABEL metadata | MISSING | No labels for maintainer/version |

**Dockerfile Score: 9/10** - Excellent. Only missing optional LABEL metadata.

### .dockerignore Analysis

| Criteria | Status | Notes |
|----------|--------|-------|
| .git excluded | PASS | Included |
| Python cache excluded | PASS | `__pycache__/`, `*.py[cod]` |
| .env excluded | PASS | `.env`, `.env.local` |
| IDE files excluded | PASS | `.vscode/`, `.idea/` |
| Tests excluded | PASS | `tests/`, `*.test.py` |
| Docs excluded | PASS | `docs/`, `*.md` |
| Data/logs excluded | PASS | `*.db`, `output/`, `data/` |
| node_modules | N/A | Not a Node project |

**.dockerignore Score: 10/10** - Comprehensive coverage.

### docker-compose.yml Analysis

| Criteria | Status | Notes |
|----------|--------|-------|
| No version field | PASS | Modern format |
| Service defined | PASS | `tlt` service |
| Build context | PASS | `.` |
| Ports exposed | PASS | 5001:5001 |
| Environment vars | PASS | Uses ${VAR} substitution |
| Secrets not hardcoded | PASS | Uses env vars |
| Volumes for data | PASS | data, output, media |
| Restart policy | PASS | `unless-stopped` |
| Healthcheck | PASS | Defined with all options |
| Read-only mount | PASS | Media mounted `:ro` |
| Resource limits | MISSING | No CPU/memory limits |
| Networks defined | N/A | Single service, not needed |

**docker-compose.yml Score: 9/10** - Strong. Consider adding resource limits for production.

### Overall Project Score: 28/30 (93%)

**Strengths:**
- Security-conscious (non-root, no hardcoded secrets, read-only mounts)
- Proper health checks in both files
- Clean cache management
- Comprehensive .dockerignore
- Modern compose format

**Recommendations:**
1. Add LABEL instructions to Dockerfile for maintainer and version info
2. Add resource limits to docker-compose.yml for production:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 512M
   ```
3. Consider creating `docker-compose.prod.yml` override for production-specific settings

## Sources

- [Docker Official Best Practices](https://docs.docker.com/build/building/best-practices/) - Core Dockerfile guidelines
- [Docker Compose in Production](https://docs.docker.com/compose/how-tos/production/) - Production compose patterns
- [Codefresh .dockerignore Guide](https://codefresh.io/blog/not-ignore-dockerignore-2/) - Why .dockerignore matters
- [Thinksys Docker Best Practices 2026](https://thinksys.com/devops/docker-best-practices/) - Modern practices overview
- [Release.com Compose Best Practices](https://release.com/blog/6-docker-compose-best-practices-for-dev-and-prod) - Multi-file compose patterns
- [Nucamp Docker 2026](https://www.nucamp.co/blog/docker-for-full-stack-developers-in-2026-containers-compose-and-production-workflows) - Current compose standards
