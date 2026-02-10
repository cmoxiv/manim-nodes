# PRD: Security & Privacy

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines security and privacy requirements for manim-nodes, focusing on safe code execution, file system protection, and network isolation for a self-hosted single-user deployment.

---

## Security Context

**Deployment Model:** Self-hosted, single-user, localhost-only
**Threat Model:** Low-risk educational tool, primary concerns are accidental misuse and safe code execution
**Compliance:** No formal requirements (personal/educational use)

---

## Security Requirements

### 1. Code Execution Safety

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-001 | Whitelist Node Types | Only allow predefined node types, no arbitrary code execution | Must |
| REQ-SEC-002 | Parameter Validation | Validate all node parameters (type, range, format) | Must |
| REQ-SEC-003 | Code Injection Prevention | Escape/sanitize all user inputs before code generation | Must |
| REQ-SEC-004 | Subprocess Sandboxing | Run MANIM CLI with limited permissions (no shell=True) | Must |
| REQ-SEC-005 | Timeout Limits | Kill renders exceeding 5 minutes (prevent infinite loops) | Must |

#### Code Injection Prevention

**Risk:** User could manipulate graph JSON to inject malicious Python code.

**Mitigation:**
```python
# ❌ BAD - vulnerable to injection
code = f"circle = Circle(radius={user_input})"

# ✅ GOOD - validated input
radius = float(user_input)  # Type validation
if not (0.1 <= radius <= 10.0):
    raise ValueError("Radius must be 0.1-10.0")
code = f"circle = Circle(radius={radius})"
```

**Validation Rules:**
- **Numbers:** Type check + range validation
- **Strings:** Escape quotes, limit length, regex pattern matching
- **Colors:** Validate hex format (`#[0-9A-Fa-f]{6}`)
- **Enums:** Whitelist allowed values

---

### 2. File System Access Control

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-006 | Restrict Write Paths | Backend can only write to designated directories | Must |
| REQ-SEC-007 | Path Traversal Prevention | Validate filenames, reject `../` patterns | Must |
| REQ-SEC-008 | File Type Restrictions | Only allow `.json` (graphs), `.mp4`, `.gif`, `.png` | Must |
| REQ-SEC-009 | Disk Quota Enforcement | Prevent unlimited file creation (10GB default limit) | Should |

#### Allowed Directories

```python
ALLOWED_PATHS = {
    "graphs": Path.home() / "manim-nodes" / "projects",
    "templates": Path.home() / "manim-nodes" / "templates",
    "exports": Path.home() / "manim-nodes" / "exports",
    "preview": Path("/tmp") / "manim-nodes" / "preview",
}

def validate_path(file_path: str, category: str) -> Path:
    """Ensure file path is within allowed directory"""
    requested = Path(file_path).resolve()
    allowed_dir = ALLOWED_PATHS[category].resolve()

    if not requested.is_relative_to(allowed_dir):
        raise SecurityError(f"Access denied: {file_path}")

    return requested
```

#### Path Traversal Prevention

```python
# ❌ BAD - vulnerable
graph_id = user_input  # e.g., "../../etc/passwd"
file_path = f"~/manim-nodes/projects/{graph_id}.json"

# ✅ GOOD - validated
import re
if not re.match(r'^[a-zA-Z0-9_-]+$', user_input):
    raise ValueError("Invalid graph ID")
graph_id = user_input
file_path = ALLOWED_PATHS["graphs"] / f"{graph_id}.json"
```

---

### 3. Network Exposure

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-010 | Localhost Binding | Bind backend to `127.0.0.1` only (no `0.0.0.0`) | Must |
| REQ-SEC-011 | No External API Calls | Backend doesn't make outbound network requests (except package installs) | Should |
| REQ-SEC-012 | CORS Restrictions | Allow only localhost origins in CORS policy | Must |

#### Localhost-Only Configuration

```python
# main.py (FastAPI backend)
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # ✅ Localhost only
        # host="0.0.0.0",  # ❌ Exposed to network
        port=8000,
    )
```

**CORS Configuration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 4. Input Validation

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-013 | Frontend Validation | Validate inputs in UI before sending to backend | Should |
| REQ-SEC-014 | Backend Validation | Re-validate all inputs on server (never trust client) | Must |
| REQ-SEC-015 | Graph Schema Validation | Use Pydantic to enforce graph structure | Must |
| REQ-SEC-016 | Max Graph Complexity | Limit nodes (200), edges (500), graph size (10MB) | Should |

#### Pydantic Schema Validation

```python
from pydantic import BaseModel, Field, validator

class NodeData(BaseModel):
    type: str = Field(..., regex=r'^[A-Za-z]+$')  # Whitelist node types
    id: str = Field(..., regex=r'^[a-zA-Z0-9_-]+$')
    position: dict[str, float]
    data: dict

    @validator('type')
    def validate_node_type(cls, v):
        allowed_types = ['Circle', 'FadeIn', 'Move', ...]  # Whitelist
        if v not in allowed_types:
            raise ValueError(f"Invalid node type: {v}")
        return v

class Graph(BaseModel):
    nodes: list[NodeData] = Field(..., max_items=200)  # Limit complexity
    edges: list[EdgeData] = Field(..., max_items=500)
    settings: dict
```

---

## Privacy Requirements

### Data Privacy

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-017 | No Telemetry | App doesn't send usage data or analytics | Must |
| REQ-SEC-018 | No External Services | No third-party integrations (except MANIM/dependencies) | Must |
| REQ-SEC-019 | Local Data Storage | All data stored on user's machine, no cloud uploads | Must |

**Rationale:** Self-hosted deployment means user owns and controls all data. No privacy concerns beyond local file permissions.

### Offline Capability (Future)

| Feature | Specification | Priority |
|---------|---------------|----------|
| **Offline Mode** | App can run without internet after initial setup | Could |
| **No CDN Dependencies** | Bundle all assets locally (no external fonts, scripts) | Could |

---

## Authentication & Authorization

### MVP (No Authentication)

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-020 | No User Accounts | Single-user deployment, no login required | Must |
| REQ-SEC-021 | Physical Access Control | Security relies on OS-level user permissions | Must |

**Rationale:** Localhost-only binding + OS user permissions = sufficient for single-user educational use.

### Future (Multi-User, Optional)

| Feature | Specification | Priority |
|---------|---------------|----------|
| **Basic Auth** | Username/password for shared deployment | Could |
| **Project Permissions** | User-specific graph ownership | Could |

---

## Dependency Security

### Dependency Management

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-022 | Pin Dependency Versions | Lock versions in `requirements.txt` / `package-lock.json` | Should |
| REQ-SEC-023 | Vulnerability Scanning (Future) | Use `pip-audit`, `npm audit` to check for CVEs | Could |
| REQ-SEC-024 | Minimal Dependencies | Avoid unnecessary packages to reduce attack surface | Should |

**Critical Dependencies:**
- MANIM Community Edition (trust official releases)
- FastAPI (well-maintained, security-focused)
- React / React Flow (large community, active security fixes)

**Dependency Updates:**
- Review changelogs before upgrading
- Test thoroughly after updates
- Pin major versions to avoid breaking changes

---

## Error Handling & Information Disclosure

### Secure Error Messages

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-025 | No Stack Traces in Production | Only show user-friendly errors in UI | Should |
| REQ-SEC-026 | Log Sensitive Errors Server-Side | Full tracebacks logged, not sent to client | Should |
| REQ-SEC-027 | Generic Error Messages | "Rendering failed" instead of "Python syntax error at line 42" | Should |

**Example:**
```python
# Backend error handling
try:
    render_animation(graph)
except Exception as e:
    logger.error(f"Render failed: {e}", exc_info=True)  # Log full traceback
    raise HTTPException(
        status_code=500,
        detail="Animation rendering failed. Check server logs."  # Generic message
    )
```

---

## Security Best Practices

### Coding Standards

| Practice | Description | Priority |
|----------|-------------|----------|
| **Input Validation** | Validate all user inputs (frontend + backend) | Must |
| **Parameterized Queries** | Use prepared statements (if database added) | N/A (no DB in MVP) |
| **Escape Outputs** | Escape HTML/JavaScript to prevent XSS | Should |
| **Avoid `eval()`** | Never use `eval()` or `exec()` on user input | Must |
| **Secure Subprocess Calls** | Use `subprocess.run(...)` with list args, no `shell=True` | Must |

### Secure Subprocess Example

```python
# ❌ BAD - vulnerable to injection
import subprocess
subprocess.run(f"manim render {user_file}", shell=True)

# ✅ GOOD - safe
subprocess.run(
    ["manim", "render", validated_file_path, "-qh"],
    shell=False,  # No shell injection
    timeout=300,  # Prevent infinite execution
    capture_output=True,
)
```

---

## Security Testing

### Manual Security Review (Pre-Release)

| Area | Checklist | Priority |
|------|-----------|----------|
| **Code Injection** | Review all code generation, ensure proper escaping | Must |
| **Path Traversal** | Test file operations with `../` payloads | Must |
| **Input Validation** | Test with invalid/malicious inputs | Must |
| **Subprocess Security** | Verify no `shell=True`, proper timeout | Must |

### Automated Scanning (Future)

| Tool | Purpose | Priority |
|------|---------|----------|
| **Bandit (Python)** | Static analysis for Python security issues | Could |
| **ESLint Security** | JavaScript/TypeScript security linting | Could |
| **npm audit** | Check for vulnerable Node.js packages | Should |
| **pip-audit** | Check for vulnerable Python packages | Should |

---

## Compliance & Audits

### MVP Requirements

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-SEC-028 | No Formal Compliance | Educational/personal use, no GDPR/HIPAA/SOC2 | N/A |
| REQ-SEC-029 | No Security Audits | Manual code review sufficient for MVP | N/A |

### Future (If Deployed as SaaS)

| Compliance | Requirements | Priority |
|------------|--------------|----------|
| **GDPR** | Data privacy, user consent, right to deletion | Could |
| **SOC 2** | Security controls for enterprise customers | Could |
| **Penetration Testing** | Third-party security assessment | Could |

---

## Incident Response (Future)

### Security Issue Handling

| Step | Action |
|------|--------|
| **Detection** | Users report issues via GitHub Issues |
| **Triage** | Assess severity (critical, high, medium, low) |
| **Fix** | Develop patch, release security update |
| **Disclosure** | Publish security advisory (GitHub Security tab) |

**Note:** Not needed for MVP (single-user deployment), but good practice for open-source release.

---

## Assumptions

- Users trust their own machines (physical access control)
- Localhost binding prevents network-based attacks
- Users don't intentionally create malicious graphs
- OS-level permissions protect sensitive files

---

## Open Questions

- [ ] Should backend support Docker deployment for additional isolation?
- [ ] Should there be a "safe mode" to review generated code before execution?
- [ ] Should graphs be digitally signed to verify authenticity?
- [ ] Should there be rate limiting on API endpoints (even for single-user)?

---

## Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Code injection via malicious graph | **High** | Low | Whitelist node types, validate params |
| Path traversal attack | **Medium** | Low | Validate filenames, restrict paths |
| Infinite loop in animation | **Medium** | Medium | Timeout limits, kill long renders |
| Dependency vulnerability | **Medium** | Medium | Pin versions, periodic audits |
| Accidental network exposure | **High** | Low | Localhost-only binding, clear docs |

---

## Security Checklist (Pre-Release)

- [ ] All user inputs validated (frontend + backend)
- [ ] No `shell=True` in subprocess calls
- [ ] File paths validated against allowed directories
- [ ] Backend bound to `127.0.0.1` only
- [ ] No `eval()` or `exec()` on user data
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies pinned to known-good versions
- [ ] Code reviewed for obvious vulnerabilities
- [ ] Tested with malicious inputs (fuzzing)
- [ ] Documentation includes security warnings

---

## Documentation Requirements

### Security Warnings for Users

Include in README and docs:

> **Security Note:** manim-nodes executes Python code generated from your graphs. Only open graphs from trusted sources. If you receive a `.json` graph file from someone else, review it carefully before opening.

> **Network Security:** By default, manim-nodes binds to `localhost` (127.0.0.1) and is not accessible from other machines. Do not change this setting unless you understand the security implications.

> **File Access:** manim-nodes can read/write files in designated directories (`~/manim-nodes/`). Do not run with elevated permissions (sudo).
