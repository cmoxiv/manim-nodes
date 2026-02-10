# PRD: Technical Architecture

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines the technical architecture, technology stack, and system design for manim-nodes.

## System Architecture

### High-Level Architecture

**Pattern:** Monolithic application (single Python backend serving frontend + API)

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          React Frontend (TypeScript)                 │   │
│  │  ├─ Node Graph Editor (React Flow)                   │   │
│  │  ├─ Property Inspector                               │   │
│  │  ├─ Animation Preview (Video Player)                 │   │
│  │  └─ WebSocket Client (real-time updates)             │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │ HTTP/WebSocket                          │
└───────────────────┼─────────────────────────────────────────┘
                    │
┌───────────────────┼─────────────────────────────────────────┐
│   Python Backend  │ (FastAPI)                               │
│  ┌────────────────▼──────────────────────────────────────┐  │
│  │              API Layer (FastAPI)                      │  │
│  │  ├─ REST Endpoints (CRUD for graphs)                 │  │
│  │  ├─ WebSocket Handler (preview streaming)            │  │
│  │  └─ Static File Server (frontend + preview frames)   │  │
│  └────────────────┬──────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼──────────────────────────────────────┐  │
│  │           Graph Processing Engine                     │  │
│  │  ├─ Graph Validator (check node connections)         │  │
│  │  ├─ Python Code Generator (nodes → MANIM script)     │  │
│  │  └─ Execution Orchestrator (run generated code)      │  │
│  └────────────────┬──────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼──────────────────────────────────────┐  │
│  │           MANIM Rendering Engine                      │  │
│  │  ├─ Preview Renderer (MANIM library, low quality)    │  │
│  │  └─ Export Renderer (MANIM CLI, high quality)        │  │
│  └────────────────┬──────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼──────────────────────────────────────┐  │
│  │              Storage Layer                            │  │
│  │  ├─ Graph Storage (JSON files on disk)               │  │
│  │  ├─ Template Library (predefined graphs)             │  │
│  │  └─ Temporary Frames (preview images, auto-cleanup)  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| **Language** | Python | 3.10+ | Native MANIM integration, ease of code generation |
| **Framework** | FastAPI | 0.104+ | Modern async support, WebSocket built-in, auto API docs |
| **MANIM** | ManimCE (Community Edition) | Latest stable | Core animation engine |
| **WebSocket** | FastAPI WebSocket (built-in) | - | Real-time preview streaming |
| **Process Management** | asyncio + subprocess | Python stdlib | Run MANIM CLI for exports |
| **File Storage** | JSON files on disk | - | Simple, no database server, good for self-hosted |

**Alternative Considered:** Flask (simpler but less async support, more manual WebSocket setup)

### Frontend

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| **Framework** | React | 18+ | Large ecosystem, mature tooling |
| **Language** | TypeScript | 5.0+ | Type safety, better developer experience |
| **Node Graph** | React Flow | 11+ | Best-in-class React node editor library |
| **State Management** | Zustand or React Query | Latest | Lightweight state (Zustand) or server state (React Query) |
| **UI Components** | Radix UI or shadcn/ui | Latest | Accessible, customizable components |
| **Build Tool** | Vite | 5.0+ | Fast dev server, modern bundler |
| **WebSocket Client** | Native WebSocket API | - | Built into browsers, no extra library |

**Alternative Considered:** Rete.js (more flexible but less React-native integration)

### Development & Deployment

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Package Manager (Backend)** | Poetry or pip + requirements.txt | Dependency management |
| **Package Manager (Frontend)** | npm or pnpm | JavaScript dependencies |
| **Containerization** | Docker + Docker Compose | Easy self-hosted deployment |
| **Python Version Manager** | pyenv (optional) | Multi-version support |
| **Code Quality** | Ruff (linter), Black (formatter), mypy (type checker) | Python code quality |
| **Frontend Linting** | ESLint + Prettier | TypeScript/React code quality |

---

## Data Architecture

### Graph Storage Format

**File Format:** JSON
**Location:** `~/manim-nodes/projects/` (user-configurable)

#### Graph Schema (JSON)

```json
{
  "id": "uuid-v4",
  "name": "My Animation",
  "version": "1.0",
  "created_at": "2026-02-07T10:30:00Z",
  "updated_at": "2026-02-07T11:45:00Z",
  "nodes": [
    {
      "id": "node-1",
      "type": "Circle",
      "position": {"x": 100, "y": 200},
      "data": {
        "radius": 2.0,
        "color": "#3498db",
        "fill_opacity": 0.5
      }
    },
    {
      "id": "node-2",
      "type": "FadeIn",
      "position": {"x": 300, "y": 200},
      "data": {
        "duration": 1.0
      }
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "sourceHandle": "output",
      "target": "node-2",
      "targetHandle": "mobject"
    }
  ],
  "settings": {
    "background_color": "#000000",
    "resolution": "1080p",
    "frame_rate": 30
  }
}
```

### Node Type Definitions

**Location:** `backend/nodes/definitions/`
**Format:** Python classes with JSON schema export

#### Example Node Definition

```python
# backend/nodes/definitions/circle.py
from pydantic import BaseModel, Field

class CircleNode(BaseModel):
    """Circle shape node"""
    node_type: str = "Circle"
    inputs: dict = {}  # No inputs for primitive shapes
    outputs: dict = {"shape": "Mobject"}

    # Parameters
    radius: float = Field(default=1.0, ge=0.1, le=10.0)
    color: str = Field(default="#FFFFFF", pattern=r"^#[0-9A-Fa-f]{6}$")
    fill_opacity: float = Field(default=0.0, ge=0.0, le=1.0)

    def to_manim_code(self, var_name: str) -> str:
        """Generate MANIM Python code"""
        return f'{var_name} = Circle(radius={self.radius}, color="{self.color}", fill_opacity={self.fill_opacity})'
```

---

## API Design

### REST Endpoints

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| GET | `/api/graphs` | List all saved graphs | - | `[{id, name, updated_at}, ...]` |
| POST | `/api/graphs` | Create new graph | `{name, nodes, edges}` | `{id, ...}` |
| GET | `/api/graphs/{id}` | Get graph by ID | - | `{id, name, nodes, edges, settings}` |
| PUT | `/api/graphs/{id}` | Update graph | `{nodes, edges, settings}` | `{id, ...}` |
| DELETE | `/api/graphs/{id}` | Delete graph | - | `204 No Content` |
| GET | `/api/templates` | List templates | - | `[{id, name, category}, ...]` |
| GET | `/api/templates/{id}` | Get template | - | `{id, name, nodes, edges}` |
| POST | `/api/export` | Export animation | `{graph_id, format, quality}` | `{job_id}` |
| GET | `/api/export/{job_id}` | Check export status | - | `{status, progress, download_url}` |
| GET | `/api/nodes/definitions` | Get all node types | - | `[{type, inputs, outputs, params}, ...]` |

### WebSocket Endpoints

| Endpoint | Purpose | Messages |
|----------|---------|----------|
| `/ws/preview` | Real-time preview streaming | Client → `{graph, quality}`<br>Server → `{frame_url, timestamp}` |

#### WebSocket Preview Flow

```
Client connects to /ws/preview
Client → {"type": "render", "graph": {...}, "quality": "medium"}
Server → {"type": "status", "message": "Rendering..."}
Server → {"type": "frame", "url": "/tmp/frames/frame_001.png", "timestamp": 0.0}
Server → {"type": "frame", "url": "/tmp/frames/frame_002.png", "timestamp": 0.033}
...
Server → {"type": "complete", "total_frames": 150, "duration": 5.0}
```

---

## Code Generation

### Graph → Python Pipeline

1. **Graph Validation**
   - Check all nodes have required inputs
   - Verify connections are type-compatible
   - Detect cycles (if not allowed)

2. **Topological Sort**
   - Order nodes by dependency (inputs before outputs)
   - Handle parallel branches

3. **Python Code Generation**
   - Generate imports: `from manim import *`
   - Create scene class: `class GeneratedScene(Scene):`
   - Generate `construct()` method with node code
   - Add error handling and logging

4. **Execution**
   - **Preview:** Import MANIM as library, render to temp frames
   - **Export:** Run MANIM CLI (`manim render script.py -qh`)

#### Example Generated Code

**Input Graph:** Circle → FadeIn → Wait → FadeOut

**Generated Python:**

```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Node: Circle (node-1)
        circle_1 = Circle(radius=2.0, color="#3498db", fill_opacity=0.5)

        # Node: FadeIn (node-2)
        self.play(FadeIn(circle_1), run_time=1.0)

        # Node: Wait (node-3)
        self.wait(2.0)

        # Node: FadeOut (node-4)
        self.play(FadeOut(circle_1), run_time=1.0)
```

---

## Rendering Strategy

### Preview Rendering (Real-Time)

| Aspect | Specification |
|--------|---------------|
| **Method** | MANIM library (import, not CLI) |
| **Quality** | Low (480p, 15fps) for speed |
| **Output** | PNG frames saved to `/tmp/manim-nodes/preview/{session_id}/` |
| **Streaming** | Serve frames via HTTP, send URLs via WebSocket |
| **Caching** | Cache identical graphs (hash-based) |
| **Cleanup** | Auto-delete frames after 1 hour |

**Performance Target:** < 2 seconds for simple animations (5-10 nodes)

### Export Rendering (High-Quality)

| Aspect | Specification |
|--------|---------------|
| **Method** | MANIM CLI subprocess (`manim render ...`) |
| **Quality** | High (1080p or 4K, 30/60fps) |
| **Output** | MP4 or GIF file in `~/manim-nodes/exports/` |
| **Progress** | Parse MANIM CLI output for progress updates |
| **Async** | Background job (user can continue editing) |

**Performance Target:** Dependent on animation complexity (1-5 minutes typical)

---

## Performance Requirements

### Backend

| Metric | Target | Notes |
|--------|--------|-------|
| **API Response Time** | < 100ms | Graph CRUD operations |
| **Preview Render Time** | < 2 seconds | Simple animations (5-10 nodes) |
| **Export Render Time** | < 5 minutes | High-quality, 30-second animation |
| **WebSocket Latency** | < 500ms | Frame delivery to browser |
| **Concurrent Users** | 1 (MVP) | Single-user local deployment |

### Frontend

| Metric | Target | Notes |
|--------|--------|-------|
| **Initial Load** | < 3 seconds | React app bundle + initial data |
| **Node Addition** | < 100ms | Drag-and-drop responsiveness |
| **Canvas Pan/Zoom** | 60fps | Smooth interaction |
| **Property Updates** | < 50ms | Immediate UI feedback |

---

## Scalability Considerations

### MVP (Single User)

- No authentication required
- Single Python process (no worker pools)
- File-based storage (no DB concurrency)
- No caching beyond preview frames

### Future Scalability (Post-MVP)

| Feature | Approach |
|---------|----------|
| **Multi-User** | Add PostgreSQL for graph storage, user authentication |
| **Concurrent Rendering** | Worker pool (Celery, RQ) for parallel renders |
| **Distributed Rendering** | Kubernetes cluster for large-scale animation farms |
| **CDN** | Serve static frontend + exports via CDN |

---

## Third-Party Integrations

### MVP Integrations

| Integration | Purpose | Priority |
|-------------|---------|----------|
| **MANIM Community Edition** | Core animation engine | Must |
| **React Flow** | Node graph editor | Must |

### Future Integrations (Post-MVP)

| Integration | Purpose | Priority |
|-------------|---------|----------|
| **FFmpeg** | Video encoding/conversion | Should |
| **LaTeX** | Math rendering (already in MANIM) | Should |
| **GitHub API** | Template sharing, version control | Could |
| **Cloud Storage (S3, GCS)** | Export storage for SaaS version | Could |

---

## Security Considerations

### Code Execution Risks

**Risk:** Generated Python code could contain malicious logic if graph is manipulated.

**Mitigation (MVP):**
- Whitelist node types (no arbitrary code execution)
- Sandboxed subprocess execution (limited permissions)
- Input validation on all node parameters (prevent injection)

**Future Mitigation:**
- Docker container per render (full isolation)
- Resource limits (CPU, memory, time)

### File System Access

**Risk:** Backend writes files to disk (graphs, frames, exports).

**Mitigation:**
- Restrict file paths to designated directories
- Validate filenames (no path traversal)
- Auto-cleanup temporary files

---

## Development Workflow

### Backend Setup

```bash
# Clone repo
git clone https://github.com/user/manim-nodes.git
cd manim-nodes

# Install Python dependencies
cd backend
poetry install  # or: pip install -r requirements.txt

# Run backend server
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
# Install Node dependencies
cd frontend
npm install

# Run dev server
npm run dev  # Vite dev server on port 5173
```

### Full Stack Development

```bash
# Use Docker Compose for integrated dev environment
docker-compose up
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

---

## Deployment Architecture

### Self-Hosted Deployment (Docker)

```yaml
# docker-compose.yml
version: '3.8'
services:
  manim-nodes:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data  # Persist graphs
      - ./exports:/app/exports  # Persist exports
    environment:
      - MANIM_QUALITY=medium
      - MAX_RENDER_TIME=300
```

**User Deployment:**
1. Install Docker + Docker Compose
2. Run `docker-compose up -d`
3. Access at `http://localhost:8000`

---

## Assumptions

- Python 3.10+ available in deployment environment
- MANIM dependencies (LaTeX, FFmpeg) installed
- Modern browsers with WebGL 2.0 and WebSocket support
- Sufficient disk space for temporary frames (~1GB recommended)
- Internet connection for initial package installation (offline after setup)

## Dependencies

### Critical Dependencies

| Dependency | Purpose | Risk if Unavailable |
|------------|---------|---------------------|
| MANIM Community Edition | Animation engine | **Critical** - project unusable |
| React Flow | Node graph UI | **High** - need alternative graph library |
| FastAPI | Backend framework | **High** - need rewrite for alternative |

### Optional Dependencies

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| FFmpeg | Video encoding | Use MANIM's built-in encoder (lower quality) |
| LaTeX | Math rendering | Text-only fallback (reduced functionality) |

---

## Open Questions

- [ ] Should backend support plugins for custom node types?
- [ ] Should preview rendering use GPU acceleration (if available)?
- [ ] Should graphs be portable across machines (absolute vs relative paths)?
- [ ] Should backend support remote MANIM rendering (offload to cloud)?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| MANIM library updates break compatibility | **High** | Pin MANIM version, automated tests for upgrades |
| Preview rendering too slow for complex graphs | **Medium** | Quality settings, caching, progress indicators |
| WebSocket connection drops during long renders | **Medium** | Reconnection logic, resume from last frame |
| Filesystem-based storage doesn't scale | **Low** | Acceptable for MVP, migrate to DB if needed |
| Generated Python code has bugs | **Medium** | Extensive testing, user-reported issues, code review |
