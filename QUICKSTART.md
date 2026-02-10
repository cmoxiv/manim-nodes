# Quick Start Guide

Get manim-nodes up and running in 5 minutes!

## Option 1: Docker (Recommended - Easiest)

If you have Docker installed, this is the fastest way to get started:

```bash
# Start the application
docker-compose up -d

# Open your browser
open http://localhost:8000
```

That's it! Everything is configured and ready to use.

To stop:
```bash
docker-compose down
```

## Option 2: Manual Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- FFmpeg (for video rendering)
- LaTeX (for mathematical text)

### Install System Dependencies

**macOS:**
```bash
brew install ffmpeg
brew install --cask mactex-no-gui
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg texlive texlive-latex-extra texlive-fonts-extra
```

### Run Setup Script

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Start Development Servers

**Terminal 1 - Backend:**
```bash
source ~/.venvs/pg/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open Browser:**
```
http://localhost:5173
```

## Creating Your First Animation

1. **Add a Circle node**
   - Look for "Shapes" category in the left panel
   - Click "Circle"
   - A circle node appears on the canvas

2. **Add a FadeIn animation**
   - Find "Animations" category
   - Click "FadeIn"
   - A FadeIn node appears

3. **Connect them**
   - Drag from the green dot on Circle (output)
   - To the blue dot on FadeIn (input)

4. **Customize the circle**
   - Click on the Circle node
   - In the right panel, change:
     - Radius: 2.0
     - Color: #00FF00 (green)
     - Fill opacity: 0.5

5. **Preview the animation**
   - Click "Render Preview" button at the top right
   - Wait a few seconds
   - Your animation plays in the preview panel!

6. **Save your work**
   - Click "Save" in the top bar
   - Your graph is automatically saved

## Next Steps

- Try adding more nodes (Text, Square, Arrow)
- Experiment with different animations (Rotate, Scale, Transform)
- Add mathematical objects (Axes, MathTex, Vector)
- Export your animation in high quality

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Check if port 5173 is already in use
lsof -i :5173

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Preview not rendering
- Make sure FFmpeg is installed: `ffmpeg -version`
- Check backend logs for errors
- Try a simpler graph first (just one Circle node)

### Docker issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f
```

## Resources

- [Full README](README.md) - Detailed documentation
- [Architecture Overview](CLAUDE.md) - Technical details
- [Node Types Reference](README.md#available-node-types) - All available nodes

## Getting Help

- Check the [GitHub Issues](https://github.com/yourusername/manim-nodes/issues)
- Review backend logs for error messages
- Ensure all dependencies are installed correctly

Happy animating! 🎬
