# Quick Start Testing Guide

## 🚀 Testing the Scene-Centric Architecture

Follow these steps to test the new implementation:

## Step 1: Start the Backend

```bash
# Activate virtual environment
source ~/.venvs/pg/bin/activate

# Start backend server
cd /Users/mo/Projects/manim-nodes
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 2: Start the Frontend

**In a new terminal:**

```bash
cd /Users/mo/Projects/manim-nodes/frontend
npm run dev
```

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Step 3: Open the Application

1. Open browser to: `http://localhost:5173`
2. You should see the **Scene Prompt Modal** appear

## Step 4: Test Scene-First Workflow

### Test 4.1: Create a Scene
1. **Expected:** Purple modal with text "Start with a Scene"
2. **Action:** Click "3D Scene with Axes"
3. **Expected:** Modal disappears, Scene node appears on canvas
4. **Verify:**
   - Node has purple border
   - Node shows "StandardScene3D" label
   - Node has two output handles:
     - Purple hexagon (scene)
     - Orange rectangle (camera)

### Test 4.2: Add a Shape
1. **Action:** Click "Nodes" panel on the left
2. **Expected:** "Scenes" category is FIRST in list with purple styling
3. **Action:** Scroll down to "Shapes 2D" category
4. **Action:** Click "+ Circle"
5. **Expected:** Circle node appears on canvas
6. **Verify:**
   - Circle node has ONE input handle on the left (scene input)
   - Circle node has ONE output handle on the right (shape output)

### Test 4.3: Connect Scene to Shape
1. **Action:** Drag from Scene's purple hexagon handle (scene output)
2. **Action:** Drop on Circle's left handle (scene input)
3. **Expected:** Edge appears connecting them
4. **Verify:** Connection is purple (scene type)

### Test 4.4: Test Validation (Negative Case)
1. **Action:** Add another Circle node (don't connect it)
2. **Expected:** No error yet (validation happens at render time)
3. **Action:** Try to render (if render button exists)
4. **Expected:** Validation error: "Shape node 'Circle' must connect to a Scene node"

## Step 5: Test Node Palette

### Test 5.1: Category Order
1. **Action:** Open Nodes panel
2. **Expected Categories in Order:**
   1. ✅ **Scenes** (purple styling)
   2. Shapes 3D
   3. Shapes 2D
   4. Text & Math
   5. Animations
   6. Camera
   7. Flow
   8. Math Ops

### Test 5.2: Scene Nodes Available
1. **Action:** Look in "Scenes" category
2. **Expected Nodes:**
   - ✅ Scene
   - ✅ StandardScene3D
   - ✅ MinimalScene
   - ✅ SceneSwitch (for future multi-scene)

## Step 6: Test Visual Styling

### Test 6.1: Handle Shapes
**Verify these handle shapes:**
- Scene output: Purple hexagon (largest)
- Camera output: Orange rectangle
- Shape (Mobject): Blue circle
- Animation: Purple triangle
- Number: Teal diamond
- Sequence: Orange square

### Test 6.2: Node Colors
**Verify node background colors:**
- Scenes: Dark purple
- Shapes 2D: Dark blue
- Shapes 3D: Dark cyan
- Animations: Dark violet
- Camera: Dark orange
- Text & Math: Dark green

## Step 7: Test Connection Menu

### Test 7.1: Smart Connection Suggestions
1. **Action:** Drag from Scene's scene output to empty space
2. **Expected:** Connection menu appears
3. **Verify:** Only shape nodes appear (Circle, Square, etc.)
4. **Action:** Close menu (Escape)

### Test 7.2: Camera Connection
1. **Action:** Drag from Scene's camera output to empty space
2. **Expected:** Connection menu appears
3. **Verify:** Only camera nodes appear (SetCameraOrientation, etc.)

## Step 8: Test Old Graph Protection

### Test 8.1: Load Old Graph (Manual API Test)
```bash
# In terminal, test the API
curl -X GET http://localhost:8000/api/graphs/some-old-graph-id
```

**Expected Response:**
```json
{
  "detail": "This graph was created with an older version and is incompatible. Please create a new graph starting with a Scene node."
}
```

## Step 9: Backend API Tests

### Test 9.1: List Nodes
```bash
curl http://localhost:8000/api/nodes | python -m json.tool | grep -A 2 "Scene"
```

**Expected:** Shows Scene node definitions

### Test 9.2: Get Scene Node Info
```bash
curl http://localhost:8000/api/nodes/Scene | python -m json.tool
```

**Expected:**
```json
{
  "type": "Scene",
  "displayName": "Scene",
  "category": "Scenes",
  "inputs": {},
  "outputs": {
    "scene": "Scene",
    "camera": "Camera"
  },
  "schema": { ... }
}
```

## Expected Results Summary

### ✅ Working Features:
- Scene-first workflow modal
- Scene node creation
- Shape nodes with scene input requirement
- Connection validation
- Visual styling (colors, handles)
- Node palette organization
- Type-safe connections

### ⚠️ Known Limitations:
- Multi-scene rendering not fully implemented (nodes exist, code generation incomplete)
- Camera wrapper classes generated on-demand (may need testing)
- No unit tests yet

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### "Module not found" errors
```bash
# Ensure virtual environment is activated
source ~/.venvs/pg/bin/activate

# Reinstall backend dependencies
pip install -r backend/requirements.txt
```

## Success Criteria

✅ **Test is SUCCESSFUL if:**
1. Scene prompt appears on empty canvas
2. Scene nodes appear first in palette with purple styling
3. Scene nodes have hexagon and rectangle handles
4. Shapes require scene connection
5. Connection menu filters by type
6. No TypeScript compilation errors

## Next Steps After Testing

If all tests pass:
1. ✅ Mark testing as complete
2. Write unit tests (tasks #15-17)
3. Update documentation (task #18)
4. Prepare for production deployment

---

**Test Status:** Ready for manual testing
**Last Updated:** 2026-02-10
