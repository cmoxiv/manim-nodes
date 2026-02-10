# Development Guide

This guide helps you contribute to manim-nodes development.

## Getting Started

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/manim-nodes.git
cd manim-nodes
./setup.sh
```

### 2. Run Development Servers

**Terminal 1 - Backend:**
```bash
source ~/.venvs/manim-nodes/bin/activate
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
manim-nodes/
├── backend/               # FastAPI backend
│   ├── api/              # REST endpoints + WebSocket
│   │   ├── graphs.py     # Graph CRUD
│   │   ├── nodes.py      # Node type listing
│   │   ├── export.py     # Export management
│   │   └── websocket.py  # Preview WebSocket
│   ├── core/             # Core business logic
│   │   ├── graph_validator.py
│   │   ├── code_generator.py
│   │   ├── renderer.py
│   │   └── storage.py
│   ├── models/           # Pydantic models
│   │   ├── graph.py
│   │   └── node.py
│   ├── nodes/            # Node type definitions
│   │   ├── base.py       # Abstract base class
│   │   ├── shapes.py     # Shape nodes
│   │   ├── animations.py # Animation nodes
│   │   └── math.py       # Math nodes
│   └── tests/            # Unit tests
│       ├── test_graph_validator.py
│       └── test_code_generator.py
│
└── frontend/             # React + TypeScript frontend
    ├── src/
    │   ├── components/   # React components
    │   │   ├── NodeEditor/
    │   │   ├── NodePalette/
    │   │   ├── AnimationPreview/
    │   │   ├── PropertyInspector/
    │   │   └── TopBar/
    │   ├── store/        # Zustand state stores
    │   │   ├── useGraphStore.ts
    │   │   ├── usePreviewStore.ts
    │   │   └── useUIStore.ts
    │   ├── api/          # API client
    │   │   └── client.ts
    │   ├── types/        # TypeScript types
    │   │   └── graph.ts
    │   └── websocket/    # WebSocket hook
    │       └── usePreviewSocket.tsx
    └── package.json
```

## Adding New Node Types

### Step 1: Create Node Class

Create a new file or add to existing in `backend/nodes/`:

```python
# backend/nodes/shapes.py

from pydantic import Field
from typing import Dict
from .base import NodeBase

class TriangleNode(NodeBase):
    """Creates a triangle shape"""
    side_length: float = Field(default=2.0, ge=0.1, le=10.0)
    color: str = Field(default="#FFFFFF")
    fill_opacity: float = Field(default=0.0, ge=0.0, le=1.0)

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = Triangle(side_length={self.side_length}, color="{self.color}", fill_opacity={self.fill_opacity})'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Shapes"
```

### Step 2: Register Node

Add to `NODE_REGISTRY` in `backend/nodes/__init__.py`:

```python
from .shapes import TriangleNode

NODE_REGISTRY = {
    # ... existing nodes ...
    "Triangle": TriangleNode,
}
```

### Step 3: Test

Restart backend and the node will automatically appear in the frontend palette!

## Node Base Class API

All nodes must extend `NodeBase` and implement:

### Required Methods

```python
def to_manim_code(self, var_name: str) -> str:
    """Generate MANIM Python code for this node"""
    pass

def get_inputs(self) -> Dict[str, str]:
    """Return input port definitions"""
    pass

def get_outputs(self) -> Dict[str, str]:
    """Return output port definitions"""
    pass
```

### Optional Methods

```python
@classmethod
def get_category(cls) -> str:
    """Return category (Shapes, Animations, Math, etc.)"""
    return "Uncategorized"

@classmethod
def get_display_name(cls) -> str:
    """Return display name (defaults to class name)"""
    return cls.__name__.replace("Node", "")
```

### Field Validation

Use Pydantic field validators:

```python
from pydantic import Field

radius: float = Field(default=1.0, ge=0.1, le=10.0)  # 0.1 to 10.0
color: str = Field(default="#FFFFFF")
fill_opacity: float = Field(default=0.0, ge=0.0, le=1.0)  # 0.0 to 1.0
```

## Input/Output Ports

### Port Types

Common port types:
- `Mobject` - Any MANIM object (shapes, text, etc.)
- `Animation` - Animation object
- `Number` - Numeric value
- `Vector` - 2D/3D vector
- `Color` - Color value

### Defining Ports

**No inputs (primitive shapes):**
```python
def get_inputs(self) -> Dict[str, str]:
    return {}
```

**Single input:**
```python
def get_inputs(self) -> Dict[str, str]:
    return {"mobject": "Mobject"}
```

**Multiple inputs:**
```python
def get_inputs(self) -> Dict[str, str]:
    return {
        "source": "Mobject",
        "target": "Mobject"
    }
```

## Code Generation

### Using Input Variables

When generating code, use placeholders for inputs:

```python
def to_manim_code(self, var_name: str) -> str:
    return f'{var_name} = FadeIn({{input_mobject}}, run_time={self.run_time})'
```

The `{input_mobject}` placeholder will be replaced with the actual variable name by the code generator.

### Animation Nodes

Animation nodes should generate code that can be passed to `self.play()`:

```python
def to_manim_code(self, var_name: str) -> str:
    return f'{var_name} = Create({{input_mobject}}, run_time={self.run_time})'
```

The code generator automatically adds `self.play()` for animation nodes.

### Shape Nodes

Shape nodes generate code that creates MANIM objects:

```python
def to_manim_code(self, var_name: str) -> str:
    return f'{var_name} = Circle(radius={self.radius})'
```

The code generator automatically adds `self.add()` for shape nodes.

## Testing

### Backend Tests

```bash
# Activate virtual environment
source ~/.venvs/manim-nodes/bin/activate

# Run all tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_graph_validator.py

# Run with coverage
pytest --cov=backend backend/tests/
```

### Writing Tests

```python
# backend/tests/test_my_node.py

from backend.nodes.shapes import TriangleNode

def test_triangle_code_generation():
    node = TriangleNode(side_length=3.0, color="#FF0000")
    code = node.to_manim_code("tri")

    assert "Triangle" in code
    assert "side_length=3.0" in code
    assert "#FF0000" in code
```

## Frontend Development

### State Management

Three Zustand stores:

1. **useGraphStore** - Graph, nodes, edges
2. **usePreviewStore** - Preview playback state
3. **useUIStore** - UI panel visibility

### Adding New Components

```typescript
// frontend/src/components/MyComponent/MyComponent.tsx

import { useGraphStore } from '../../store/useGraphStore';

export default function MyComponent() {
  const nodes = useGraphStore((state) => state.nodes);

  return (
    <div className="p-4">
      <h2>My Component</h2>
      <p>Nodes: {nodes.length}</p>
    </div>
  );
}
```

### API Calls

Use the API client:

```typescript
import { apiClient } from '../api/client';

// In component
const handleSave = async () => {
  try {
    await apiClient.updateGraph(graph.id, graph);
  } catch (error) {
    console.error('Save failed:', error);
  }
};
```

## Debugging

### Backend Debugging

Add logging:
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Debug message here")
```

View logs in terminal where backend is running.

### Frontend Debugging

Use browser DevTools:
- Console: `console.log()`
- React DevTools: Inspect component state
- Network tab: Check API requests

### WebSocket Debugging

Check WebSocket messages:
```typescript
// In usePreviewSocket.tsx
ws.current.addEventListener('message', (event) => {
  console.log('WebSocket message:', event.data);
  // ... handle message
});
```

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Docstrings for classes and public methods
- Line length: 100 characters

```python
def my_function(param: str) -> int:
    """
    Short description.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    return 42
```

### TypeScript (Frontend)

- Use functional components with hooks
- Prefer `const` over `let`
- Use TypeScript strict mode
- Destructure props

```typescript
interface MyProps {
  title: string;
  count: number;
}

export default function MyComponent({ title, count }: MyProps) {
  const [value, setValue] = useState(0);

  return <div>{title}: {count}</div>;
}
```

## Common Tasks

### Reset Development Environment

```bash
# Backend
rm -rf ~/.venvs/manim-nodes
./setup.sh

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Clear Generated Files

```bash
# Clear MANIM cache
rm -rf ~/manim-nodes/temp/

# Clear saved graphs
rm -rf ~/manim-nodes/projects/
```

### Update Dependencies

```bash
# Backend
pip install --upgrade -r backend/requirements.txt

# Frontend
cd frontend
npm update
```

## Deployment

### Docker Build

```bash
# Build image
docker-compose build

# Start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production Considerations

For production deployment:

1. **Environment Variables**
   - Set `DATA_DIR`, `EXPORT_DIR`
   - Configure CORS origins in `main.py`

2. **Reverse Proxy**
   - Use Nginx for HTTPS
   - Proxy `/api` and `/ws` to backend

3. **Security**
   - Add authentication
   - Rate limiting
   - Input sanitization

4. **Monitoring**
   - Log aggregation
   - Error tracking (Sentry)
   - Performance monitoring

## Getting Help

- Check [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for current progress
- Review [QUICKSTART.md](QUICKSTART.md) for setup issues
- Open GitHub issue for bugs
- Discussions for questions

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Write tests if applicable
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open Pull Request

## License

MIT License - see LICENSE file for details.
