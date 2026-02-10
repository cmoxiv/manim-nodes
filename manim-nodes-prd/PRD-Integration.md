# PRD: Integration & Deployment

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines deployment strategies, environment configuration, and integration requirements for manim-nodes.

---

## Deployment Strategies

### Supported Deployment Methods

| ID | Method | Description | Priority | Target Users |
|----|--------|-------------|----------|--------------|
| REQ-DEP-001 | Docker Container | `docker-compose up` - one-command setup | Must | All users (recommended) |
| REQ-DEP-002 | Manual Setup | Clone repo, install dependencies, run servers | Must | Developers, advanced users |
| REQ-DEP-003 | Python Package (Future) | `pip install manim-nodes` + CLI | Could | Python users |
| REQ-DEP-004 | Pre-built Binary (Future) | Standalone executable (Electron/PyInstaller) | Could | Non-technical users |

---

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Install system dependencies (MANIM requirements)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend
COPY backend/ ./backend/
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build (pre-built in CI or locally)
COPY frontend/dist ./frontend/dist

# Expose port
EXPOSE 8000

# Run backend (serves frontend static files)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  manim-nodes:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data              # Persist graphs
      - ./exports:/app/exports        # Persist exports
      - /tmp/manim-nodes:/tmp/manim-nodes  # Preview frames
    environment:
      - MANIM_QUALITY=medium
      - MAX_RENDER_TIME=300
      - DATA_DIR=/app/data
    restart: unless-stopped
```

### User Instructions (README)

```markdown
## Quick Start (Docker)

1. Install Docker and Docker Compose
2. Clone repository:
   ```bash
   git clone https://github.com/user/manim-nodes.git
   cd manim-nodes
   ```
3. Build and run:
   ```bash
   docker-compose up -d
   ```
4. Open browser: http://localhost:8000
```

---

## Manual Deployment

### Backend Setup

```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Install MANIM (if not already installed)
pip install manim

# 3. Run backend server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup

```bash
# 1. Install Node.js dependencies
cd frontend
npm install

# 2. Build frontend (production)
npm run build

# OR run dev server (development)
npm run dev
```

### System Requirements

| Requirement | Specification |
|-------------|---------------|
| **Python** | 3.10 or higher |
| **Node.js** | 18 or higher |
| **FFmpeg** | Latest stable (for MANIM) |
| **LaTeX** | texlive-full (for MANIM math rendering) |
| **Disk Space** | 2GB minimum (dependencies + temp files) |
| **RAM** | 4GB minimum, 8GB recommended |
| **OS** | macOS, Linux, Windows (WSL2) |

---

## Environment Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATA_DIR` | Directory for saved graphs | `~/manim-nodes/projects` | No |
| `EXPORT_DIR` | Directory for exported videos | `~/manim-nodes/exports` | No |
| `PREVIEW_DIR` | Directory for preview frames | `/tmp/manim-nodes/preview` | No |
| `MANIM_QUALITY` | Default preview quality | `medium` | No |
| `MAX_RENDER_TIME` | Render timeout (seconds) | `300` | No |
| `HOST` | Backend bind address | `127.0.0.1` | No |
| `PORT` | Backend port | `8000` | No |

### Configuration File (Optional)

```yaml
# config.yml
directories:
  data: ~/manim-nodes/projects
  exports: ~/manim-nodes/exports
  preview: /tmp/manim-nodes/preview

rendering:
  quality: medium
  max_time: 300
  frame_rate: 30

server:
  host: 127.0.0.1
  port: 8000
  cors_origins:
    - http://localhost:5173
```

---

## CI/CD Pipeline

### MVP Approach

**Strategy:** Manual testing and releases (no automated CI/CD)

**Release Process:**
1. Manual testing (functional, cross-browser)
2. Version bump (semver: `v0.1.0`, `v0.2.0`, etc.)
3. Git tag: `git tag v0.1.0 && git push --tags`
4. GitHub Release with binaries (Docker image, source code)

### Future CI/CD (GitHub Actions)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Build Docker image
      - name: Build Docker image
        run: docker build -t manim-nodes:${{ github.ref_name }} .

      # Push to Docker Hub (optional)
      - name: Push to Docker Hub
        run: docker push manim-nodes:${{ github.ref_name }}

      # Create GitHub Release
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          body: See CHANGELOG.md for details
```

---

## Environment Strategy

### Environments

| Environment | Purpose | Configuration |
|-------------|---------|---------------|
| **Development** | Local development (hot reload) | Vite dev server (frontend), uvicorn --reload (backend) |
| **Production** | User deployment (Docker or manual) | Built frontend, optimized backend |

**Note:** No staging environment needed for single-user self-hosted deployment.

---

## Monitoring & Logging

### MVP Logging

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-DEP-005 | Console Logs | stdout/stderr for debugging | Must |
| REQ-DEP-006 | File Logs | Rotating logs in `~/manim-nodes/logs/` | Should |
| REQ-DEP-007 | Error Tracking | Capture exceptions with tracebacks | Must |

**Log Rotation:**
```python
# backend/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "~/manim-nodes/logs/app.log",
    maxBytes=100_000_000,  # 100MB per file
    backupCount=5,         # Keep 5 old files
)
logging.basicConfig(handlers=[handler], level=logging.INFO)
```

### Future Monitoring (Optional)

| Tool | Purpose |
|------|---------|
| **Prometheus** | Metrics (API response times, render queue length) |
| **Grafana** | Dashboards for visualization |
| **Sentry** | Error tracking and alerting |

---

## Rollback & Recovery

### Rollback Procedure

**Scenario:** New version has critical bug

**Steps:**
1. Stop service: `docker-compose down`
2. Checkout previous version: `git checkout v0.1.0`
3. Rebuild: `docker-compose build`
4. Restart: `docker-compose up -d`

### Data Backup

| Data | Backup Strategy | Priority |
|------|-----------------|----------|
| **Saved Graphs** | User responsible (manual backup of `~/manim-nodes/projects/`) | Should |
| **Exports** | User responsible (exports in `~/manim-nodes/exports/`) | Could |
| **Config** | Version controlled (config.yml in repo) | Should |

**Recommendation:** Users should periodically back up `~/manim-nodes/` directory.

---

## Infrastructure Requirements

### Local Deployment (Single User)

**Resources:**
- CPU: 2+ cores (rendering benefits from multiple cores)
- RAM: 4GB minimum, 8GB recommended
- Disk: 10GB free space (MANIM dependencies + temp files)
- Network: Internet for initial setup (offline after dependencies installed)

### Cloud Deployment (Future - Multi-User SaaS)

**Scenario:** Hosted service for multiple users

**Infrastructure:**
| Component | Service | Specification |
|-----------|---------|---------------|
| **Compute** | AWS EC2, GCP Compute Engine | t3.medium (2 vCPU, 4GB RAM) minimum |
| **Storage** | S3, GCS | For graphs, exports, backups |
| **Database** | PostgreSQL (RDS, Cloud SQL) | For user accounts, metadata |
| **Load Balancer** | ALB, Cloud Load Balancing | Distribute traffic |
| **Container Orchestration** | Kubernetes, ECS | Scalable rendering workers |

---

## Deployment Checklist

### Pre-Deployment

- [ ] All tests pass (unit, integration, manual)
- [ ] Code reviewed and merged to main
- [ ] Version bumped (package.json, pyproject.toml)
- [ ] CHANGELOG.md updated
- [ ] Documentation updated (README, user guide)
- [ ] Docker image builds successfully
- [ ] Tested on clean machine (no cached dependencies)

### Post-Deployment

- [ ] Verify application starts correctly
- [ ] Smoke test (create graph, preview, export)
- [ ] Check logs for errors
- [ ] Monitor for first 24 hours

---

## Assumptions

- Users can install Docker (or have Python 3.10+ for manual setup)
- Users have stable internet connection for initial setup
- macOS/Linux preferred (Windows via WSL2)

---

## Open Questions

- [ ] Should Docker image be published to Docker Hub for easier access?
- [ ] Should there be automatic update notifications (check GitHub releases)?
- [ ] Should deployment support custom domain/SSL (for shared deployments)?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Docker installation too complex for non-technical users | **Medium** | Provide detailed setup guide, video tutorial |
| MANIM dependencies fail to install | **High** | Pin dependency versions, provide troubleshooting guide |
| Port 8000 already in use on user's machine | **Low** | Allow port configuration via env var |
| Disk fills up with temp files | **Medium** | Auto-cleanup, disk usage warnings |
