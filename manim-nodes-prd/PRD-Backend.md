# PRD: Backend Requirements

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document specifies the backend server requirements for manim-nodes, including API design, data processing, rendering, and file management.

---

## Server Architecture

### Core Components

| ID | Component | Description | Technology | Priority |
|----|-----------|-------------|------------|----------|
| REQ-BE-001 | API Server | REST endpoints + WebSocket handler | FastAPI | Must |
| REQ-BE-002 | Graph Processing Engine | Validate, sort, generate Python code | Python (custom) | Must |
| REQ-BE-003 | MANIM Rendering Engine | Execute generated code, produce frames | MANIM library + CLI | Must |
| REQ-BE-004 | File Storage Manager | Save/load graphs, manage temp files | Python (os, pathlib) | Must |
| REQ-BE-005 | Background Job Queue | Async export rendering | asyncio (MVP), Celery (future) | Should |

---

## Authentication & Authorization

### MVP Requirements

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-BE-006 | No Authentication | Single-user local deployment - no login required | Must |
| REQ-BE-007 | Localhost-Only Binding (Optional) | Bind to 127.0.0.1 to prevent network access | Should |

**Rationale:** Self-hosted single-user deployment doesn't require authentication. Security via localhost binding only.

### Future (Post-MVP)

| Feature | Purpose | Priority |
|---------|---------|----------|
| Multi-User Auth | Username/password login for shared deployment | Could |
| API Keys | Programmatic access control | Could |
| SSO Integration | Enterprise deployment | Could |

---

## API Endpoints (Detailed)

### Graph Management

#### `POST /api/graphs`
**Create New Graph**

**Request:**
```json
{
  "name": "My Animation",
  "nodes": [...],
  "edges": [...],
  "settings": {...}
}
```

**Response (201 Created):**
```json
{
  "id": "uuid-v4",
  "name": "My Animation",
  "created_at": "2026-02-07T10:30:00Z",
  "updated_at": "2026-02-07T10:30:00Z"
}
```

**Validation:**
- Name required (1-100 characters)
- Nodes/edges must conform to schema
- No circular dependencies (if not allowed)

---

#### `GET /api/graphs`
**List All Graphs**

**Response (200 OK):**
```json
[
  {
    "id": "uuid-1",
    "name": "Pythagorean Theorem",
    "updated_at": "2026-02-07T10:30:00Z",
    "node_count": 15,
    "preview_url": "/api/graphs/uuid-1/thumbnail"
  },
  ...
]
```

**Query Parameters:**
- `sort` (optional): `name`, `updated_at` (default)
- `order` (optional): `asc`, `desc` (default: `desc`)

---

#### `GET /api/graphs/{id}`
**Get Graph by ID**

**Response (200 OK):**
```json
{
  "id": "uuid-1",
  "name": "Pythagorean Theorem",
  "nodes": [...],
  "edges": [...],
  "settings": {...},
  "created_at": "2026-02-07T09:00:00Z",
  "updated_at": "2026-02-07T10:30:00Z"
}
```

**Error (404 Not Found):**
```json
{
  "error": "Graph not found",
  "id": "uuid-1"
}
```

---

#### `PUT /api/graphs/{id}`
**Update Graph**

**Request:**
```json
{
  "name": "Updated Name",
  "nodes": [...],
  "edges": [...],
  "settings": {...}
}
```

**Response (200 OK):**
```json
{
  "id": "uuid-1",
  "updated_at": "2026-02-07T11:00:00Z"
}
```

---

#### `DELETE /api/graphs/{id}`
**Delete Graph**

**Response (204 No Content)**

**Side Effects:**
- Deletes graph file from disk
- Deletes associated preview frames (if any)

---

### Template Library

#### `GET /api/templates`
**List Available Templates**

**Response (200 OK):**
```json
[
  {
    "id": "template-1",
    "name": "Linear Algebra - Matrix Multiplication",
    "category": "Math",
    "description": "Visualize matrix multiplication step-by-step",
    "thumbnail_url": "/static/templates/template-1-thumb.png"
  },
  ...
]
```

**Categories:** Math, Physics, ML/AI, General

---

#### `GET /api/templates/{id}`
**Get Template Graph**

**Response (200 OK):**
```json
{
  "id": "template-1",
  "name": "Linear Algebra - Matrix Multiplication",
  "nodes": [...],
  "edges": [...],
  "settings": {...},
  "instructions": "Customize the matrix values in the Matrix nodes..."
}
```

---

### Export & Rendering

#### `POST /api/export`
**Start Export Job**

**Request:**
```json
{
  "graph_id": "uuid-1",
  "format": "mp4",  // or "gif"
  "quality": "1080p",  // or "720p", "4k"
  "frame_rate": 30  // or 60
}
```

**Response (202 Accepted):**
```json
{
  "job_id": "job-uuid",
  "status": "queued",
  "estimated_time": 120  // seconds
}
```

**Background Processing:**
- Job runs asynchronously
- User can continue editing other graphs
- WebSocket notification on completion

---

#### `GET /api/export/{job_id}`
**Check Export Status**

**Response (200 OK):**
```json
{
  "job_id": "job-uuid",
  "status": "completed",  // or "queued", "rendering", "failed"
  "progress": 100,  // percentage (0-100)
  "download_url": "/exports/job-uuid.mp4",
  "file_size": 15728640,  // bytes
  "created_at": "2026-02-07T11:00:00Z",
  "completed_at": "2026-02-07T11:03:45Z"
}
```

**Error Response (failed job):**
```json
{
  "job_id": "job-uuid",
  "status": "failed",
  "error": "MANIM rendering failed: Invalid radius value (-5)",
  "traceback": "File \"scene.py\", line 12..."
}
```

---

### Node Definitions

#### `GET /api/nodes/definitions`
**Get All Node Types**

**Response (200 OK):**
```json
[
  {
    "type": "Circle",
    "category": "Shapes",
    "inputs": {},
    "outputs": {
      "shape": "Mobject"
    },
    "parameters": [
      {
        "name": "radius",
        "type": "number",
        "default": 1.0,
        "min": 0.1,
        "max": 10.0,
        "description": "Circle radius"
      },
      {
        "name": "color",
        "type": "color",
        "default": "#FFFFFF",
        "description": "Circle color"
      }
    ],
    "documentation": "Creates a circle shape",
    "example_code": "circle = Circle(radius=2.0, color=BLUE)"
  },
  ...
]
```

---

## WebSocket API

### `/ws/preview`

**Purpose:** Real-time preview frame streaming

#### Client → Server Messages

**Render Request:**
```json
{
  "type": "render",
  "graph": {
    "nodes": [...],
    "edges": [...],
    "settings": {...}
  },
  "quality": "medium"  // or "low", "high"
}
```

**Cancel Request:**
```json
{
  "type": "cancel"
}
```

#### Server → Client Messages

**Status Update:**
```json
{
  "type": "status",
  "message": "Validating graph...",
  "progress": 10
}
```

**Frame Update:**
```json
{
  "type": "frame",
  "url": "/tmp/preview/session-xyz/frame_015.png",
  "frame_number": 15,
  "timestamp": 0.5,  // seconds
  "total_frames": 150
}
```

**Completion:**
```json
{
  "type": "complete",
  "total_frames": 150,
  "duration": 5.0,  // seconds
  "preview_url": "/tmp/preview/session-xyz/"
}
```

**Error:**
```json
{
  "type": "error",
  "message": "Rendering failed: Circle requires positive radius",
  "node_id": "node-5",
  "traceback": "..."
}
```

---

## Graph Processing Engine

### Graph Validation

| ID | Validation Rule | Error Response |
|----|-----------------|----------------|
| REQ-BE-008 | All required inputs connected | "Node 'FadeIn' missing required input 'mobject'" |
| REQ-BE-009 | Type compatibility (Shape → Shape, Number → Number) | "Cannot connect Color to Number" |
| REQ-BE-010 | No circular dependencies (if disallowed) | "Circular dependency detected: node-1 → node-2 → node-1" |
| REQ-BE-011 | Valid parameter values (min/max, patterns) | "Circle radius must be > 0, got -5" |

### Topological Sorting

**Purpose:** Order nodes by dependency for sequential execution

**Algorithm:**
1. Build dependency graph (edges define "depends on")
2. Kahn's algorithm (or DFS-based topological sort)
3. Detect cycles (error if found)
4. Return ordered node list

**Example:**
```
Input Graph:
  A → B → D
  A → C → D

Topological Order: [A, B, C, D] (or [A, C, B, D])
```

### Python Code Generation

| ID | Component | Description | Priority |
|----|-----------|-------------|----------|
| REQ-BE-012 | Code Template | Base scene class with imports | Must |
| REQ-BE-013 | Node Code Generators | Each node type has `.to_manim_code()` method | Must |
| REQ-BE-014 | Variable Naming | Auto-generate unique variable names (node type + ID) | Must |
| REQ-BE-015 | Error Handling | Wrap generated code in try/except | Should |

**Generated Code Structure:**
```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        try:
            # Generated node code here
            circle_1 = Circle(radius=2.0)
            self.play(FadeIn(circle_1))
            ...
        except Exception as e:
            print(f"Animation error: {e}")
            raise
```

---

## MANIM Rendering

### Preview Rendering (Library Mode)

| ID | Specification | Value | Priority |
|----|---------------|-------|----------|
| REQ-BE-016 | Rendering Method | Import MANIM as library, call `Scene.render()` | Must |
| REQ-BE-017 | Quality | Low (480p, 15fps) | Must |
| REQ-BE-018 | Output Format | PNG frames | Must |
| REQ-BE-019 | Output Location | `/tmp/manim-nodes/preview/{session_id}/` | Must |
| REQ-BE-020 | Timeout | 30 seconds max (prevent infinite loops) | Should |

**Process:**
1. Generate Python code from graph
2. Import code as module
3. Instantiate `GeneratedScene`
4. Call `render()` with low-quality settings
5. Stream frame URLs via WebSocket as they're created

**Performance Target:** < 2 seconds for simple animations (5-10 nodes)

---

### Export Rendering (CLI Mode)

| ID | Specification | Value | Priority |
|----|---------------|-------|----------|
| REQ-BE-021 | Rendering Method | Subprocess call to `manim render ...` | Must |
| REQ-BE-022 | Quality | High (1080p or 4K, 30/60fps) | Must |
| REQ-BE-023 | Output Format | MP4 (H.264) or GIF | Must |
| REQ-BE-024 | Output Location | `~/manim-nodes/exports/{job_id}.{ext}` | Must |
| REQ-BE-025 | Background Execution | Async job (doesn't block API) | Must |
| REQ-BE-026 | Progress Tracking | Parse MANIM CLI output for progress | Should |

**Process:**
1. Generate Python code, save to temp file
2. Queue background job
3. Run `manim render script.py -qh -o output.mp4` (subprocess)
4. Parse CLI output for progress updates
5. Notify via WebSocket when complete
6. Return download URL

**Performance Target:** < 5 minutes for 30-second, 1080p animation

---

## Background Jobs

### Job Queue System (MVP)

| ID | Requirement | Specification | Priority |
|----|-------------|---------------|----------|
| REQ-BE-027 | Queue Implementation | Python `asyncio` task queue (simple) | Must |
| REQ-BE-028 | Concurrency | Single worker (one export at a time) | Must |
| REQ-BE-029 | Job Persistence | In-memory only (lost on restart) | Must |
| REQ-BE-030 | Status Tracking | Job status stored in dict (queued, rendering, completed, failed) | Must |

**Queuing Logic:**
- New export request → Add to queue
- If queue empty → start immediately
- Else → wait for current job to finish
- Update job status via polling or WebSocket

### Future (Post-MVP)

| Feature | Technology | Priority |
|---------|------------|----------|
| Persistent Queue | Celery + Redis/RabbitMQ | Should |
| Multiple Workers | Parallel exports (configurable pool size) | Should |
| Job Retry | Auto-retry failed jobs (3 attempts) | Could |

---

## File Storage & Management

### Storage Structure

```
~/manim-nodes/
├── projects/
│   ├── {graph-id}.json          # Saved graphs
│   └── ...
├── templates/
│   ├── template-1.json
│   └── ...
├── exports/
│   ├── {job-id}.mp4
│   ├── {job-id}.gif
│   └── ...
└── tmp/
    └── preview/
        ├── {session-id}/
        │   ├── frame_001.png
        │   ├── frame_002.png
        │   └── ...
        └── ...
```

### File Management Policies

| ID | Policy | Specification | Priority |
|----|--------|---------------|----------|
| REQ-BE-031 | Preview Frame Cleanup | Auto-delete frames > 1 hour old | Must |
| REQ-BE-032 | Export Cleanup | Auto-delete exports > 7 days old (user-configurable) | Should |
| REQ-BE-033 | Disk Quota Warnings | Warn if total storage > 10GB (configurable) | Should |
| REQ-BE-034 | Manual Cleanup Endpoint | `POST /api/cleanup` - force cleanup | Could |

**Cleanup Process:**
- Run periodic background task (every 10 minutes)
- Scan `/tmp/preview/` for old directories
- Delete directories older than 1 hour
- Scan `/exports/` for old files (if auto-delete enabled)
- Check total disk usage, log warning if quota exceeded

---

## Logging & Monitoring

### Logging Requirements

| ID | Log Type | Destination | Format | Priority |
|----|----------|-------------|--------|----------|
| REQ-BE-035 | Console Logs | stdout/stderr | Human-readable | Must |
| REQ-BE-036 | File Logs | `~/manim-nodes/logs/app.log` | Structured JSON | Must |
| REQ-BE-037 | Rotating Logs | Max 100MB per file, keep 5 files | Rotation policy | Should |
| REQ-BE-038 | Error Tracking | Capture exceptions + stack traces | JSON with traceback | Must |

### Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| **DEBUG** | Detailed diagnostic info | "Generating code for node Circle (node-5)" |
| **INFO** | Normal operations | "Graph saved: uuid-123", "Export started: job-456" |
| **WARNING** | Potential issues | "Disk usage at 85%", "Slow render: 15 seconds" |
| **ERROR** | Recoverable errors | "Graph validation failed: missing input", "Render timeout" |
| **CRITICAL** | System failures | "MANIM not found", "Cannot write to disk" |

### Structured Log Format (JSON)

```json
{
  "timestamp": "2026-02-07T11:30:00Z",
  "level": "ERROR",
  "message": "Render failed for graph uuid-123",
  "context": {
    "graph_id": "uuid-123",
    "job_id": "job-456",
    "error": "Circle radius must be positive",
    "traceback": "..."
  }
}
```

### Monitoring Metrics (Future)

| Metric | Purpose | Tool |
|--------|---------|------|
| API Response Time | Detect slow endpoints | Prometheus + Grafana |
| Render Queue Length | Monitor backlog | Custom metrics |
| Disk Usage | Prevent storage exhaustion | OS-level monitoring |
| Error Rate | Detect reliability issues | Error tracking service |

---

## Performance Requirements

### API Response Times

| Endpoint | Target | Max Acceptable |
|----------|--------|----------------|
| `GET /api/graphs` | < 50ms | 200ms |
| `POST /api/graphs` | < 100ms | 500ms |
| `GET /api/graphs/{id}` | < 50ms | 200ms |
| `GET /api/nodes/definitions` | < 20ms (cached) | 100ms |
| `POST /api/export` (queue job) | < 100ms | 500ms |

### Rendering Performance

| Operation | Target | Max Acceptable |
|-----------|--------|----------------|
| Preview Render (simple graph) | < 2 seconds | 5 seconds |
| Preview Render (complex graph) | < 5 seconds | 15 seconds |
| Export Render (30sec, 1080p) | < 3 minutes | 10 minutes |
| Code Generation | < 100ms | 500ms |

---

## Error Handling

### Error Response Format

**Standard Error Response:**
```json
{
  "error": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional context"
  },
  "request_id": "uuid-request"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `GRAPH_NOT_FOUND` | 404 | Graph ID doesn't exist |
| `VALIDATION_ERROR` | 400 | Graph validation failed |
| `RENDER_FAILED` | 500 | MANIM rendering error |
| `TIMEOUT` | 504 | Render exceeded time limit |
| `DISK_FULL` | 507 | Insufficient storage |

### Error Recovery

| Error Type | Recovery Strategy |
|------------|-------------------|
| **Validation Errors** | Return detailed error, highlight problematic nodes in UI |
| **Render Timeouts** | Cancel render, return partial results if available |
| **Disk Full** | Trigger cleanup, warn user, suggest manual deletion |
| **MANIM Crashes** | Capture traceback, log error, suggest debugging steps |

---

## Dependencies & Integrations

### Critical Dependencies

| Dependency | Version | Purpose | Fallback |
|------------|---------|---------|----------|
| MANIM Community Edition | Latest stable | Animation rendering | **None** - critical |
| FastAPI | 0.104+ | Web framework | **None** - critical |
| Pydantic | 2.0+ | Data validation | **None** - critical |

### Optional Dependencies

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| FFmpeg | Video encoding (via MANIM) | MANIM's built-in encoder |
| LaTeX | Math rendering (via MANIM) | Text-only mode (degraded) |

---

## Assumptions

- Python 3.10+ installed
- MANIM and dependencies (FFmpeg, LaTeX) pre-installed
- Sufficient disk space for temporary frames (~1GB minimum)
- Single-user local deployment (no authentication needed)
- Localhost binding prevents unauthorized access

---

## Open Questions

- [ ] Should backend support graph versioning (history of edits)?
- [ ] Should backend cache generated Python code for identical graphs?
- [ ] Should export jobs support cancellation mid-render?
- [ ] Should backend support custom MANIM plugins/extensions?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| MANIM rendering hangs indefinitely | **High** | Timeout limits, process monitoring |
| Generated code has syntax errors | **Medium** | Extensive testing, linting generated code |
| Disk fills up with temp files | **Medium** | Auto-cleanup, disk quota warnings |
| Export queue grows too long | **Low** | Single-user deployment unlikely to hit this |
