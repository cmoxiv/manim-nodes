# PRD: Testing & Quality

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines testing strategy, quality standards, and quality gates for manim-nodes.

---

## Testing Strategy

### Approach

**Focus:** Unit tests for critical paths, manual testing for user workflows
**Coverage:** No strict target, prioritize high-risk areas (code generation, validation)
**Automation:** Automated unit tests + manual E2E testing

---

## Test Types

### 1. Unit Tests

| ID | Test Area | Description | Priority | Tools |
|----|-----------|-------------|----------|-------|
| REQ-TEST-001 | Graph Validation | Test node/edge validation logic | Must | pytest |
| REQ-TEST-002 | Code Generation | Test Python code generation from graphs | Must | pytest |
| REQ-TEST-003 | Node Definitions | Test each node type's `.to_manim_code()` | Must | pytest |
| REQ-TEST-004 | Topological Sort | Test dependency ordering algorithm | Must | pytest |
| REQ-TEST-005 | Input Validation | Test parameter validation (types, ranges) | Must | pytest, Pydantic |
| REQ-TEST-006 | React Components | Test UI component rendering | Should | Jest, React Testing Library |

**Example Unit Test:**
```python
# tests/test_code_generation.py
def test_circle_code_generation():
    node = CircleNode(radius=2.0, color="#3498db")
    code = node.to_manim_code("circle_1")
    assert 'circle_1 = Circle(radius=2.0' in code
    assert 'color="#3498db"' in code

def test_graph_validation_missing_input():
    graph = {
        "nodes": [{"id": "1", "type": "FadeIn", "data": {}}],
        "edges": []
    }
    with pytest.raises(ValidationError, match="missing required input"):
        validate_graph(graph)
```

---

### 2. Integration Tests (Future)

| Test Area | Description | Priority |
|-----------|-------------|----------|
| API Endpoints | Test REST endpoints (graph CRUD) | Should |
| WebSocket Flow | Test preview rendering via WebSocket | Should |
| File Operations | Test save/load graph to disk | Should |

---

### 3. End-to-End Tests (Manual)

| Workflow | Test Steps | Priority |
|----------|------------|----------|
| **Create Simple Animation** | Add Circle → FadeIn → Export MP4 → Verify output | Must |
| **Load Template** | Open template → Customize → Preview → Export | Must |
| **Error Handling** | Create invalid graph → Verify error shown | Must |
| **Auto-Save** | Edit graph → Wait 2 sec → Verify saved to backend | Should |

---

## Code Coverage

### Target

**Coverage Goal:** No strict percentage target
**Focus:** Cover critical paths:
- Graph validation (100%)
- Code generation (100%)
- Node definitions (80%+)
- API endpoints (60%+)

**Tools:**
- Backend: `pytest-cov`
- Frontend: Jest coverage reports

**Example:**
```bash
# Backend coverage
pytest --cov=backend --cov-report=html

# Frontend coverage
npm run test -- --coverage
```

---

## Quality Gates

### Pre-Merge Requirements

| ID | Gate | Description | Priority | Enforcement |
|----|------|-------------|----------|-------------|
| REQ-QA-001 | Linting Passes | Python: Ruff/Black, TypeScript: ESLint/Prettier | Must | CI/local hooks |
| REQ-QA-002 | Type Checking Passes | Python: mypy (optional), TypeScript: tsc | Should | CI |
| REQ-QA-003 | Unit Tests Pass | All automated tests green | Must | CI |
| REQ-QA-004 | Code Review | Human review + approval | Must | GitHub PR |

### Linting Configuration

**Backend (Python):**
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I"]  # Pyflakes, pycodestyle, import sorting

[tool.black]
line-length = 100
```

**Frontend (TypeScript):**
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

---

## Testing Tools

### Backend (Python)

| Tool | Purpose |
|------|---------|
| **pytest** | Test framework |
| **pytest-cov** | Code coverage |
| **pytest-asyncio** | Async test support |
| **Faker** | Generate test data |
| **httpx** | Test FastAPI endpoints |

### Frontend (TypeScript/React)

| Tool | Purpose |
|------|---------|
| **Jest** | Test framework |
| **React Testing Library** | Component testing |
| **@testing-library/user-event** | Simulate user interactions |
| **Mock Service Worker (MSW)** | Mock API requests |

---

## Quality Standards

### Code Style

| Language | Standards |
|----------|-----------|
| **Python** | PEP 8, Black formatting, 100-char line length |
| **TypeScript** | ESLint rules, Prettier formatting |
| **React** | Functional components, hooks, TypeScript props |

### Documentation Standards

| ID | Requirement | Description | Priority |
|----|-------------|-------------|----------|
| REQ-QA-005 | Docstrings (Python) | All public functions have docstrings | Should |
| REQ-QA-006 | JSDoc (TypeScript) | Complex functions documented | Could |
| REQ-QA-007 | README | Setup instructions, architecture overview | Must |
| REQ-QA-008 | API Docs | FastAPI auto-generates OpenAPI docs | Must |

**Example Docstring:**
```python
def generate_code(graph: Graph) -> str:
    """
    Generate MANIM Python code from node graph.

    Args:
        graph: Validated graph with nodes and edges

    Returns:
        Executable Python code string

    Raises:
        ValidationError: If graph is invalid
        CodeGenerationError: If code generation fails
    """
    ...
```

---

## Performance Testing (Future)

### Performance Benchmarks

| Metric | Target | Priority |
|--------|--------|----------|
| Preview Render Time (simple graph) | < 2 seconds | Should |
| API Response Time (graph save) | < 100ms | Should |
| Frontend Initial Load | < 3 seconds | Could |

**Tool:** `pytest-benchmark` for backend, Lighthouse for frontend

---

## Manual Testing Checklist (Pre-Release)

### Functional Tests

- [ ] Create new graph from scratch
- [ ] Load existing graph
- [ ] Add nodes from palette
- [ ] Connect nodes (drag wire)
- [ ] Edit node properties
- [ ] Preview animation (live update)
- [ ] Export to MP4
- [ ] Export to GIF
- [ ] Load template
- [ ] Save graph (manual + auto-save)
- [ ] Delete graph
- [ ] Keyboard shortcuts work (Ctrl+S, Delete, etc.)

### Error Handling Tests

- [ ] Create invalid graph (missing required input)
- [ ] Test with invalid parameter values (negative radius)
- [ ] Test network disconnection (WebSocket recovery)
- [ ] Test disk full scenario (prevent crash)
- [ ] Test MANIM render failure (show error)

### Cross-Browser Tests

- [ ] Chrome (primary)
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Performance Tests

- [ ] Large graph (100+ nodes) - verify reasonable performance
- [ ] Long animation (60 seconds) - verify export works
- [ ] Rapid edits - verify debounced updates

---

## Continuous Integration (Future)

### CI Pipeline (GitHub Actions Example)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint
        run: ruff check .
      - name: Type check
        run: mypy backend/
      - name: Run tests
        run: pytest --cov=backend

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Lint
        run: npm run lint
      - name: Type check
        run: npm run type-check
      - name: Run tests
        run: npm test
```

---

## Bug Tracking & Issue Management

### Issue Labels (GitHub)

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or request |
| `documentation` | Improvements or additions to docs |
| `good first issue` | Good for newcomers |
| `critical` | Blocking issue, high priority |

### Bug Report Template

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create graph with nodes...
2. Click export...
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. macOS 14]
 - Python version: [e.g. 3.10]
 - MANIM version: [e.g. 0.18.0]
```

---

## Assumptions

- Developers have Python 3.10+ and Node.js 18+ installed
- Tests run locally before pushing (pre-commit hooks optional)
- CI/CD is future enhancement (MVP can skip)

---

## Open Questions

- [ ] Should there be visual regression testing (screenshot comparison)?
- [ ] Should tests include example MANIM animations to verify output quality?
- [ ] Should there be load testing for concurrent users (even if single-user MVP)?
- [ ] Should CI run on multiple OS (macOS, Linux, Windows)?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Test suite becomes slow | **Medium** | Parallelize tests, mock expensive operations |
| Low test coverage misses bugs | **Medium** | Focus on critical paths, manual testing |
| CI/CD setup overhead | **Low** | Start with local testing, add CI post-MVP |
