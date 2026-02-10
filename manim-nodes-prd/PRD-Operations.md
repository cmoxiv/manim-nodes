# PRD: Operations & Support

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines operational requirements, support model, and documentation needs for manim-nodes.

---

## Support Model

### MVP Support Strategy

**Model:** Community support via GitHub Issues (experimental project)

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-OPS-001 | GitHub Issues | Primary support channel for bug reports and questions | Must |
| REQ-OPS-002 | No SLA | No guaranteed response time (best-effort support) | N/A |
| REQ-OPS-003 | Community-Driven | Users help each other, maintainer responds when available | Should |

**Support Scope:**
- ✅ Bug reports (reproducible issues)
- ✅ Feature requests (community discussion)
- ✅ Installation help (setup issues)
- ❌ Custom development (user-specific features)
- ❌ Live chat/phone support (not available)

---

## Documentation Requirements

### 1. README.md

| ID | Section | Description | Priority |
|----|---------|-------------|----------|
| REQ-OPS-004 | Project Overview | What is manim-nodes, who it's for | Must |
| REQ-OPS-005 | Quick Start | Docker setup instructions | Must |
| REQ-OPS-006 | Manual Setup | Alternative installation (Python + Node.js) | Must |
| REQ-OPS-007 | Architecture | High-level system design diagram | Should |
| REQ-OPS-008 | Contributing | How to contribute (for open source) | Should |
| REQ-OPS-009 | License | MIT or similar permissive license | Must |

**Example README Structure:**
```markdown
# manim-nodes

Visual programming interface for creating MANIM animations.

## Features
- Drag-and-drop node editor
- Live animation preview
- Export to MP4/GIF
- No coding required

## Quick Start (Docker)
\`\`\`bash
docker-compose up -d
# Open http://localhost:8000
\`\`\`

## Manual Setup
See [INSTALL.md](INSTALL.md) for detailed instructions.

## Documentation
- [User Guide](docs/user-guide.md)
- [Node Library Reference](docs/nodes.md)
- [Architecture](docs/architecture.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
MIT
```

---

### 2. User Guide (docs/user-guide.md)

| Section | Description | Priority |
|---------|-------------|----------|
| **Getting Started** | First animation tutorial | Must |
| **Node Library** | Description of each node type | Must |
| **Keyboard Shortcuts** | List of shortcuts | Should |
| **Templates** | How to use and create templates | Should |
| **Export Settings** | Quality, format options | Must |
| **Troubleshooting** | Common issues and solutions | Must |

**Example Tutorial:**
```markdown
## Creating Your First Animation

1. **Add a Circle**
   - Search for "Circle" in the node palette (left sidebar)
   - Drag it to the canvas
   - Adjust radius and color in the property inspector

2. **Add FadeIn Animation**
   - Search for "FadeIn"
   - Drag it to the canvas
   - Connect Circle output to FadeIn input (drag wire)

3. **Preview**
   - Animation appears in preview panel (right side)
   - Click Play to watch

4. **Export**
   - Click Export button (top bar)
   - Select MP4, 1080p, 30fps
   - Wait for render to complete
   - Download video
```

---

### 3. API Documentation

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-OPS-010 | Auto-Generated API Docs | FastAPI `/docs` endpoint (Swagger UI) | Must |
| REQ-OPS-011 | Endpoint Descriptions | Docstrings for all API routes | Should |
| REQ-OPS-012 | Request/Response Examples | Sample JSON payloads | Should |

**Auto-generated docs available at:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

### 4. Video Tutorials (Future)

| Tutorial | Description | Duration | Priority |
|----------|-------------|----------|----------|
| **Quick Start** | Install and create first animation | 5 min | Should |
| **Node Library Tour** | Overview of available nodes | 10 min | Could |
| **Live Teaching Demo** | Using manim-nodes in classroom | 15 min | Could |
| **Advanced Workflows** | Templates, custom nodes (future) | 20 min | Could |

---

## Uptime & Reliability

### SLA (Service Level Agreement)

**MVP:** No SLA (local deployment, user controls uptime)

**Future (SaaS):**
| Metric | Target | Measurement |
|--------|--------|-------------|
| **Uptime** | 99.5% | Monthly availability |
| **API Response** | < 200ms (p95) | Average API latency |
| **Render Success Rate** | > 95% | Successful exports / total requests |

---

## Disaster Recovery

### Backup Strategy

| Data | Backup Method | Frequency | Priority |
|------|---------------|-----------|----------|
| **User Graphs** | User manual backup of `~/manim-nodes/projects/` | Ad-hoc | Should |
| **Config** | Version controlled in Git | Per commit | Must |
| **Templates** | Bundled in repository | Per release | Must |

**Recommendation for Users:**
```bash
# Backup command (add to cron for automation)
tar -czf manim-nodes-backup-$(date +%Y%m%d).tar.gz ~/manim-nodes/projects/
```

### Recovery Procedure

**Scenario:** User's system crashes, needs to restore graphs

**Steps:**
1. Reinstall manim-nodes (Docker or manual)
2. Extract backup: `tar -xzf manim-nodes-backup-20260207.tar.gz`
3. Copy to data directory: `cp -r projects/* ~/manim-nodes/projects/`
4. Restart application

---

## Maintenance & Updates

### Update Frequency

| Type | Frequency | Trigger |
|------|-----------|---------|
| **Patch Releases** | As needed | Critical bug fixes |
| **Minor Releases** | Monthly (post-MVP) | New features, improvements |
| **Major Releases** | Quarterly | Breaking changes, major features |

### Update Notification

| ID | Method | Description | Priority |
|----|--------|-------------|----------|
| REQ-OPS-013 | GitHub Releases | Users watch repo for notifications | Must |
| REQ-OPS-014 | CHANGELOG.md | Document all changes | Must |
| REQ-OPS-015 | In-App Notification (Future) | Check for updates on startup | Could |

**Example CHANGELOG:**
```markdown
# Changelog

## [0.2.0] - 2026-03-15

### Added
- Template library with 10 pre-built animations
- Keyboard shortcuts (Ctrl+S, Ctrl+Z, etc.)
- Export progress bar

### Fixed
- Preview not updating on property change
- WebSocket reconnection issues

## [0.1.0] - 2026-02-15

### Added
- Initial MVP release
- Node graph editor
- Live preview
- Export to MP4/GIF
```

---

## Monitoring & Alerts (Future)

### Health Checks

| Metric | Check | Alert Threshold |
|--------|-------|----------------|
| **Service Status** | HTTP ping to `/health` | Down > 1 minute |
| **Disk Usage** | Check free space | < 1GB remaining |
| **Render Queue** | Queue length | > 10 pending jobs |
| **Error Rate** | Count 500 errors | > 5 errors/minute |

**Health Endpoint:**
```python
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "disk_free_gb": get_disk_free(),
        "queue_length": get_queue_length(),
    }
```

---

## Training & Onboarding

### For End Users

| Resource | Description | Priority |
|----------|-------------|----------|
| **Interactive Tutorial** | In-app walkthrough (future) | Could |
| **Example Graphs** | Pre-loaded examples to explore | Should |
| **Video Tutorials** | YouTube series (5-15 min each) | Should |

### For Contributors (Future)

| Resource | Description | Priority |
|----------|-------------|----------|
| **CONTRIBUTING.md** | Code style, PR process, development setup | Should |
| **Architecture Docs** | System design, code organization | Should |
| **Node Development Guide** | How to add custom nodes | Could |

---

## Issue Triage & Resolution

### Issue Labels (GitHub)

| Label | Description | SLA (Future) |
|-------|-------------|--------------|
| `critical` | Blocker, app unusable | 24 hours |
| `bug` | Something broken | 1 week |
| `enhancement` | New feature request | Backlog |
| `documentation` | Docs improvement | 2 weeks |
| `good first issue` | Easy for newcomers | N/A |

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what's wrong.

**To Reproduce**
1. Create graph with Circle node
2. Set radius to -5
3. Click preview

**Expected behavior**
Should show error message.

**Actual behavior**
App crashes.

**Environment**
- OS: macOS 14
- manim-nodes version: 0.1.0
- Python version: 3.10
- MANIM version: 0.18.0

**Logs**
Paste relevant logs here.
```

---

## Community Engagement (Future)

### Communication Channels

| Channel | Purpose | Priority |
|---------|---------|----------|
| **GitHub Discussions** | Q&A, feature discussions | Should |
| **Discord Server** | Real-time chat, community | Could |
| **Twitter/X** | Announcements, showcases | Could |

### Contribution Opportunities

| Type | Description |
|------|-------------|
| **Bug Fixes** | Fix reported issues |
| **New Nodes** | Add MANIM primitives to node library |
| **Templates** | Create example animations |
| **Documentation** | Improve guides and tutorials |
| **Translations** | Internationalization (future) |

---

## Assumptions

- Users comfortable with command-line (or can follow Docker instructions)
- Users willing to self-troubleshoot using documentation
- No 24/7 support team (single maintainer or small team)
- Community will contribute once project gains traction

---

## Open Questions

- [ ] Should there be a user forum (Discourse, Reddit) for discussions?
- [ ] Should there be a showcase gallery (user-submitted animations)?
- [ ] Should there be a newsletter for major updates?
- [ ] Should there be sponsored/paid support for enterprise users?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Insufficient documentation leads to support burden | **High** | Comprehensive docs, FAQ, video tutorials |
| Users expect professional support (not available) | **Medium** | Clearly state "experimental, community support only" |
| Community doesn't form (low adoption) | **Medium** | Marketing (Reddit, HN), quality docs, polish MVP |
| Maintainer burnout (single person project) | **High** | Set expectations, accept contributions, consider co-maintainers |

---

## Success Metrics (Post-Launch)

### Adoption Metrics

| Metric | Target (6 months) | Measurement |
|--------|-------------------|-------------|
| **GitHub Stars** | 100+ | Community interest |
| **Installations** | 500+ | Docker pulls, downloads |
| **Active Users** | 50+ | GitHub Issues, Discussions activity |
| **Contributions** | 5+ external contributors | PRs from community |

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Bug Report Resolution** | < 2 weeks (average) | GitHub Issues |
| **Documentation Completeness** | 90%+ features documented | Manual review |
| **User Satisfaction** | 4/5 stars (if survey) | Feedback surveys |
