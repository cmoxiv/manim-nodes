# Project Requirement Document: manim-nodes

> Version: 1.0
> Date: 2026-02-07
> Status: Draft - Ready for Review

---

## Executive Summary

**manim-nodes** is a self-hosted web application that democratizes mathematical animation creation by providing a visual, node-based programming interface to the MANIM animation engine. It removes the coding barrier for educators, content creators, and researchers, enabling them to create publication-quality animations through an intuitive drag-and-drop interface.

### Vision

Transform how mathematical and ML concepts are visualized by making MANIM accessible to non-programmers while maintaining the power and flexibility of programmatic animations.

### Key Value Propositions

1. **No Code Required:** Visual node-based interface - drag, drop, and connect
2. **Live Preview:** Real-time animation updates as you build
3. **Rapid Iteration:** Instant feedback eliminates slow code-compile-preview cycles
4. **Educational Focus:** Built for teaching - live classroom demos, step-by-step execution
5. **Extensible:** Domain-specific nodes for math, physics, ML; custom node creation

### Target Users

- **Math/CS Instructors:** Creating lecture animations and live classroom demonstrations
- **Content Creators:** YouTubers and online educators producing educational videos
- **Researchers:** Academics visualizing concepts for papers and presentations

### MVP Timeline

**1-2 months** to basic MVP with:
- Node graph editor with 20-30 core nodes
- Live preview with WebSocket streaming
- Export to MP4/GIF
- Docker deployment for easy setup

---

## Table of Contents

1. [Product Vision](PRD-Product.md) - Problem statement, target users, success metrics
2. [Features & User Stories](PRD-Features.md) - Functional requirements, user workflows
3. [User Experience](PRD-UX.md) - UI/UX design, interaction patterns
4. [Technical Architecture](PRD-Technical.md) - System design, technology stack
5. [Backend Requirements](PRD-Backend.md) - API design, rendering engine, storage
6. [Frontend Requirements](PRD-Frontend.md) - React components, state management
7. [Security & Privacy](PRD-Security.md) - Code execution safety, file access control
8. [Testing & Quality](PRD-Testing.md) - Testing strategy, quality gates
9. [Integration & Deployment](PRD-Integration.md) - Deployment methods, CI/CD
10. [Operations & Support](PRD-Operations.md) - Documentation, support model

---

## Key Requirements Summary

### Must-Have (MVP)

#### Core Functionality
- **Node Graph Editor:** Drag-and-drop canvas with React Flow
- **Node Library:** 20-30 core MANIM primitives (shapes, animations, math)
- **Live Preview:** Real-time WebSocket-based animation streaming
- **Property Inspector:** Edit node parameters (colors, sizes, positions)
- **Export:** Render to MP4 and GIF (1080p, 30/60fps)
- **Save/Load:** Persist graphs as JSON files

#### Architecture
- **Backend:** Python 3.10+ with FastAPI, MANIM library integration
- **Frontend:** React 18+ with TypeScript, React Flow, Tailwind CSS
- **Deployment:** Docker container (one-command setup) + manual setup option
- **Storage:** File-based (JSON graphs on disk, no database)

#### User Experience
- **Three-Panel Layout:** Node Palette (left) + Editor (center) + Preview (right)
- **Auto-Save:** Debounced auto-save (2 sec) + manual save button
- **Keyboard Shortcuts:** Ctrl+S, Ctrl+Z, Delete, etc.
- **Error Handling:** Visual node highlighting, user-friendly error messages

### Should-Have (Post-MVP)

- **Template Library:** Pre-built animation examples
- **Node Search:** Fuzzy search palette for quick node discovery
- **Step-by-Step Execution:** Run graph node-by-node for live teaching
- **Export Python Code:** Show generated MANIM script (educational)
- **Snapshots:** Save intermediate graph states
- **Undo/Redo:** Full history stack

### Could-Have (Future)

- **Custom Node Creation:** User-defined nodes with Python plugins
- **Presentation Mode:** Fullscreen preview, hide editor
- **Collaborative Editing:** Real-time multi-user editing
- **Python Package:** `pip install manim-nodes` CLI tool
- **Mobile/Tablet Support:** Touch-optimized interface

---

## Technical Stack

### Backend
| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10+ |
| **Framework** | FastAPI |
| **Animation Engine** | MANIM Community Edition |
| **WebSocket** | FastAPI built-in |
| **Storage** | JSON files (filesystem) |

### Frontend
| Component | Technology |
|-----------|------------|
| **Framework** | React 18+ |
| **Language** | TypeScript 5.0+ |
| **Build Tool** | Vite |
| **Node Graph** | React Flow |
| **UI Components** | Radix UI / shadcn/ui |
| **Styling** | Tailwind CSS |
| **State Management** | Zustand |

### Deployment
| Component | Technology |
|-----------|------------|
| **Container** | Docker + Docker Compose |
| **Package Manager (Backend)** | pip |
| **Package Manager (Frontend)** | npm |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (React)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Node Editor (React Flow) │ Preview (Video Player)  │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │ HTTP/WebSocket                              │
└───────────────┼─────────────────────────────────────────────┘
                │
┌───────────────┼─────────────────────────────────────────────┐
│  Backend      │ (FastAPI + MANIM)                           │
│  ┌────────────▼──────────────────────────────────────────┐  │
│  │  API: Graph CRUD, Export, Templates                   │  │
│  │  WebSocket: Live preview streaming                    │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│  ┌────────────▼──────────────────────────────────────────┐  │
│  │  Graph Processor: Validate → Sort → Generate Python   │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│  ┌────────────▼──────────────────────────────────────────┐  │
│  │  MANIM Renderer: Preview (library) + Export (CLI)     │  │
│  └────────────┬──────────────────────────────────────────┘  │
│               │                                              │
│  ┌────────────▼──────────────────────────────────────────┐  │
│  │  Storage: Graphs (JSON), Exports (MP4/GIF), Frames    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## User Workflows

### Workflow 1: Create Animation from Scratch
1. Launch manim-nodes (`http://localhost:8000`)
2. Search node palette for "Circle"
3. Drag Circle to canvas, set radius = 2.0, color = Blue
4. Search for "FadeIn", drag to canvas
5. Connect Circle output → FadeIn input (wire)
6. Preview auto-updates → shows blue circle fading in
7. Click Export → select MP4, 1080p → download video

**Target Time:** 5-10 minutes

### Workflow 2: Use Template
1. Click "File" → "Open Template"
2. Select "Linear Algebra - Matrix Multiplication"
3. Edit matrix values in property inspector
4. Preview updates with new values
5. Export → download video

**Target Time:** 2-5 minutes

### Workflow 3: Live Classroom Demo
1. Launch manim-nodes, share screen with students
2. Build graph incrementally while explaining concept
3. Use step-by-step execution to show animation building
4. Export final animation + Python code to share

**Target Time:** 15-20 minutes

---

## Success Criteria

### Functional Requirements
- ✅ Non-programmers create first animation in < 30 minutes
- ✅ Generated animations match quality of hand-coded MANIM
- ✅ Preview updates within 2 seconds for simple graphs
- ✅ Export completes within 5 minutes for 30-second animations

### User Adoption (6 months post-launch)
- **GitHub Stars:** 100+
- **Installations:** 500+
- **Active Users:** 50+
- **Community Contributors:** 5+

### Quality Metrics
- **Bug Resolution:** < 2 weeks average
- **Test Coverage:** Critical paths 100%, overall 60%+
- **Documentation:** All features documented

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **UX too complex for non-technical users** | High | User testing with instructors; simplified default view |
| **MANIM API changes break compatibility** | High | Pin MANIM version; adapter layer |
| **Preview latency frustrates users** | High | Quality settings; debounced updates; optimize rendering |
| **Installation too difficult** | Medium | Docker one-command setup; detailed troubleshooting docs |
| **Code injection vulnerabilities** | High | Whitelist node types; validate all inputs; sandboxed execution |

---

## Open Questions

### Technical
- [ ] Should backend support GPU acceleration for MANIM rendering?
- [ ] Should graphs be shareable via URL (requires backend storage changes)?
- [ ] Should custom node creation use Python plugins or visual node builder?

### Product
- [ ] Should MVP support mobile/tablet interfaces, or desktop-only?
- [ ] What's the maximum animation length supported (30 sec? 60 sec? unlimited)?
- [ ] Should there be a graph marketplace for sharing templates?

### Deployment
- [ ] Should Docker image be published to Docker Hub?
- [ ] Should there be automatic update notifications?
- [ ] Should deployment support custom domain/SSL for shared use?

---

## Dependencies

### Critical (Blockers)
- **MANIM Community Edition:** Core animation engine - no alternative
- **React Flow:** Node graph UI - alternatives exist but require significant rework
- **FastAPI:** Backend framework - alternatives exist but require rewrite

### Important (Substitutable)
- **Zustand:** State management - could use Redux, Context
- **Radix UI:** UI components - could build custom
- **Docker:** Deployment - could use manual setup only

---

## Next Steps

### Phase 1: Requirements Finalization (Current)
- ✅ Complete PRD interview (10 aspects)
- ⏳ Review PRD with stakeholders
- ⏳ Finalize MVP scope and timeline

### Phase 2: Design & Planning (Week 1-2)
- Create wireframes and mockups
- Define node type specifications (20-30 core nodes)
- Set up development environment (Git repo, Docker, CI)
- Create implementation plan (see separate document)

### Phase 3: Implementation (Week 3-8)
- **Sprint 1-2 (Week 3-4):** Backend API + graph processing
- **Sprint 3-4 (Week 5-6):** Frontend UI + node editor
- **Sprint 5-6 (Week 7-8):** Preview rendering + export
- **Sprint 7-8 (Week 9-10):** Polish, testing, documentation

### Phase 4: Testing & Launch (Week 9-10)
- Manual testing (functional, cross-browser)
- Documentation (README, user guide, video tutorials)
- Docker packaging and deployment testing
- GitHub release (v0.1.0 MVP)

---

## Appendices

### Glossary

| Term | Definition |
|------|------------|
| **MANIM** | Mathematical Animation Engine (Python library for creating animations) |
| **Node Graph** | Visual programming paradigm where operations are nodes connected by wires |
| **Mobject** | MANIM Mathematical Object (shapes, text, etc.) |
| **Scene** | MANIM animation container (equivalent to one video output) |
| **Topological Sort** | Algorithm to order nodes by dependencies |

### Reference Documents

- [MANIM Community Edition Docs](https://docs.manim.community/)
- [React Flow Documentation](https://reactflow.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Interview Notes

**Date:** 2026-02-07
**Participants:** Product Owner, Development Team
**Key Decisions:**
- MVP timeline: 1-2 months (aggressive but achievable)
- Deployment: Docker primary, manual setup secondary
- Security: Localhost-only, no authentication for MVP
- Support: Community-driven, no SLA
- Testing: Unit tests for critical paths, manual E2E testing

---

**Document Status:** Draft - Awaiting Approval
**Next Review:** After stakeholder review
**Approved By:** _______________
**Date:** _______________
