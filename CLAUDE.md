# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**manim-nodes** - A visual programming interface for creating MANIM animations through a drag-and-drop node-based interface. Built with FastAPI (backend) and React + TypeScript (frontend).

## Setup Instructions

### Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv ~/.venvs/pg
source ~/.venvs/pg/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the backend server (from project root)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Common Commands

```bash
# Backend (make sure to activate venv first: source ~/.venvs/pg/bin/activate)
uvicorn backend.main:app --reload              # Run backend dev server
pytest backend/                                # Run backend tests

# Frontend
npm run dev                                    # Run frontend dev server
npm run build                                  # Build for production
npm run lint                                   # Lint TypeScript/React

# Docker
docker-compose up -d                          # Start services
docker-compose down                           # Stop services
docker-compose logs -f                        # View logs
```

## Architecture

### Backend (`/backend`)

- **FastAPI application** with REST API and WebSocket support
- **Core modules:**
  - `api/` - REST endpoints (graphs, nodes, export) + WebSocket handler
  - `core/` - Business logic (validation, code generation, rendering)
  - `models/` - Pydantic data models
  - `nodes/` - Node type definitions (shapes, animations, math)
- **Storage:** File-based JSON storage in `~/manim-nodes/`
- **Rendering:** MANIM CE for animation generation

### Frontend (`/frontend`)

- **React 18 + TypeScript** with Vite build tool
- **Key libraries:**
  - React Flow - Node editor
  - Zustand - State management
  - TailwindCSS - Styling
  - ReconnectingWebSocket - WebSocket client
- **State stores:**
  - `useGraphStore` - Graph/node/edge state
  - `usePreviewStore` - Preview playback state
  - `useUIStore` - UI panel visibility

### Data Flow

1. User creates graph in React Flow editor
2. Graph auto-saves to backend via REST API
3. User clicks "Render Preview" → WebSocket sends graph
4. Backend generates Python code from graph
5. MANIM renders animation (low quality for preview)
6. Video URL streamed back via WebSocket
7. Frontend displays video in preview panel

## Development Notes

### Adding New Node Types

1. Create node class in `backend/nodes/[category].py`
2. Extend `NodeBase` abstract class
3. Implement: `to_manim_code()`, `get_inputs()`, `get_outputs()`
4. Add to `NODE_REGISTRY` in `backend/nodes/__init__.py`
5. Restart backend - node appears automatically in frontend

### Code Style

- **Backend:** Follow PEP 8, use type hints
- **Frontend:** Use TypeScript strict mode, functional components with hooks
- **Naming:** snake_case (Python), camelCase (TypeScript)

### Testing

- Backend unit tests in `backend/tests/`
- Test critical paths: validation, code generation, rendering
- Manual E2E testing for frontend workflow

### Deployment

- Primary: Docker Compose (single command)
- Manual setup documented in README
- No authentication in MVP (localhost-only binding)
