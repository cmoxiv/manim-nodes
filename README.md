# Manim Nodes

A visual programming interface for creating MANIM animations through a drag-and-drop node-based interface. Perfect for educators, content creators, and researchers who want to create mathematical animations without writing code.

## Features

- 🎨 **Visual Node Editor**: Drag-and-drop interface powered by React Flow
- 🎬 **Live Preview**: Real-time preview of animations via WebSocket
- 📦 **20+ Node Types**: Shapes, animations, math objects, and more
- 💾 **Auto-Save**: Automatic graph saving with dirty state tracking
- 📤 **Export**: High-quality video export (480p to 4K, 15-60fps)
- 🐳 **Docker Support**: One-command deployment with Docker Compose
- 🎯 **Type Safety**: Full TypeScript support in frontend

## Quick Start

### Docker (Recommended)

The easiest way to run Manim Nodes:

```bash
# Clone the repository
git clone https://github.com/yourusername/manim-nodes.git
cd manim-nodes

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

That's it! The application will be running with all dependencies installed.

### Manual Setup

If you prefer not to use Docker:

#### Backend Setup

```bash
# Create Python virtual environment
python3 -m venv ~/.venvs/manim-nodes
source ~/.venvs/manim-nodes/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# Install Node dependencies
cd frontend
npm install

# Run the development server
npm run dev
```

Access the application at http://localhost:5173

## System Requirements

- **Docker**: Latest version (recommended)
- **Python**: 3.10+ (for manual setup)
- **Node.js**: 18+ (for manual setup)
- **FFmpeg**: Required for video rendering
- **LaTeX**: Required for mathematical text rendering

## Usage

### Creating Your First Animation

1. **Add Nodes**: Click nodes from the left palette to add them to the canvas
2. **Connect Nodes**: Drag from output handles (green) to input handles (blue)
3. **Edit Properties**: Select a node and modify its properties in the right panel
4. **Preview**: Click "Render Preview" to see your animation
5. **Export**: Click "Export" to generate high-quality video

### Example: Simple Circle Animation

1. Add a **Circle** node from the Shapes category
2. Add a **FadeIn** node from the Animations category
3. Connect Circle's output to FadeIn's input
4. Click "Render Preview"

### Keyboard Shortcuts

- `Ctrl/Cmd + S`: Save graph
- `Delete`: Delete selected nodes
- `Space`: Play/pause preview
- `Esc`: Deselect nodes

## Available Node Types

### Shapes
- Circle, Square, Rectangle
- Line, Arrow
- Text

### Animations
- FadeIn, FadeOut
- Create, Write
- Transform
- Rotate, Scale
- MoveTo

### Math
- Axes, NumberPlane
- MathTex (LaTeX support)
- Vector, Dot

## Architecture

**Backend:**
- FastAPI (REST API + WebSocket)
- MANIM CE (animation rendering)
- Pydantic (data validation)

**Frontend:**
- React 18 + TypeScript
- React Flow (node editor)
- Zustand (state management)
- TailwindCSS (styling)

**Deployment:**
- Docker + Docker Compose
- Nginx (reverse proxy, optional)

## Development

### Project Structure

```
manim-nodes/
├── backend/
│   ├── api/              # REST API endpoints
│   ├── core/             # Core logic (validation, code gen, rendering)
│   ├── models/           # Pydantic models
│   ├── nodes/            # Node definitions
│   └── main.py           # FastAPI app entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── store/        # Zustand stores
│   │   ├── api/          # API client
│   │   └── types/        # TypeScript types
│   └── package.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend linting
cd frontend
npm run lint
```

### Adding New Nodes

1. Create a new node class in `backend/nodes/`
2. Extend `NodeBase` and implement required methods
3. Add to `NODE_REGISTRY` in `backend/nodes/__init__.py`
4. Restart backend - node will appear in frontend palette automatically

Example:

```python
from .base import NodeBase
from pydantic import Field

class MyCustomNode(NodeBase):
    my_param: float = Field(default=1.0)

    def to_manim_code(self, var_name: str) -> str:
        return f'{var_name} = MyManimObject(param={self.my_param})'

    def get_inputs(self) -> Dict[str, str]:
        return {}

    def get_outputs(self) -> Dict[str, str]:
        return {"shape": "Mobject"}

    @classmethod
    def get_category(cls) -> str:
        return "Custom"
```

## Troubleshooting

### Video rendering fails
- Ensure FFmpeg is installed: `ffmpeg -version`
- Check LaTeX installation: `latex --version`
- Review render logs in preview panel

### WebSocket connection issues
- Check backend is running: `curl http://localhost:8000/health`
- Verify firewall settings
- Check browser console for errors

### Slow preview rendering
- Preview uses low quality (480p, 15fps) for speed
- Complex scenes may still take time
- Use simpler graphs during development

## Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with [MANIM Community Edition](https://www.manim.community/)
- Node editor powered by [React Flow](https://reactflow.dev/)
- Inspired by visual programming tools like Blender's Geometry Nodes

## Support

- 📖 Documentation: [GitHub Wiki](https://github.com/yourusername/manim-nodes/wiki)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/manim-nodes/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/manim-nodes/discussions)

---

Made with ❤️ for the MANIM community
