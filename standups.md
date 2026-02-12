# Development Standups

## 2026-02-09

### What Got Done

**Code Viewer Feature - Complete Implementation:**
- ✅ Modified backend to return generated Python code alongside video files
  - Updated `backend/core/renderer.py` to return tuple `(Path, str)` from all render methods
  - Modified WebSocket handler to include code in "complete" message
- ✅ Built full-featured code viewer component with syntax highlighting
  - Integrated `react-syntax-highlighter` with VS Code Dark Plus theme
  - Added copy-to-clipboard functionality with success feedback
  - Implemented download-as-.py with filename sanitization
- ✅ Redesigned UI architecture for canvas/code view switching
  - Added `mainView` state to `useUIStore` for canvas/code toggling
  - Created Canvas/Code toggle buttons in top bar with icons
  - Code viewer now replaces node canvas instead of being a tab in preview panel
- ✅ Implemented proper scrolling for large generated code files
  - Fixed header with flex-shrink-0
  - Scrollable content area with overflow-auto and min-h-0
- ✅ Verified Manim-CE (Cairo renderer) configuration for documentation

### Summary

Completed full implementation of the code viewer feature for manim-nodes, allowing users to view, copy, and download generated MANIM Python code. The viewer replaces the node canvas with a dedicated code view accessible via top-bar toggle, featuring syntax highlighting, proper scrolling, and export functionality.

## 2026-02-09 15:45

**Branch:** Not a git repository

### Completed
- Conducted comprehensive code review of manim-nodes codebase
- Identified 6 critical security vulnerabilities (arbitrary code execution via unsanitized node inputs)
- Identified 14 warnings across performance, code quality, and architecture
- Identified 10 suggestions for improvements
- Documented findings with specific file locations and severity ratings

### In Progress
- Recent dependency installation in frontend (node_modules updates for syntax highlighting)
- Code review findings awaiting action

### Blockers
- None

### Next Steps
- Fix critical security vulnerability: Add regex validators to all `color` fields across node types
- Sanitize text input fields in TextNode and MathTexNode to prevent code injection
- Fix CORS configuration to restrict origins and remove credential allowance
- Add subprocess timeouts and rate limiting to WebSocket endpoint
- Implement performance optimizations (node lookup dictionary, deque for topological sort)

## Session Wrap-up - 2026-02-09

**Date:** 2026-02-09

### What Got Done

**Performance & Code Quality Improvements:**
- ✅ Optimized node lookups from O(n²) to O(1) using dictionary maps
- ✅ Replaced inefficient `list.pop(0)` with `collections.deque` in topological sort
- ✅ Eliminated duplicate cycle detection with caching
- ✅ Added Python logging framework replacing print() statements
- ✅ Migrated from deprecated `@app.on_event` to FastAPI `lifespan` context manager
- ✅ Implemented StorageManager dependency injection across all endpoints
- ✅ Replaced `Date.now()` with `crypto.randomUUID()` for collision-safe IDs in frontend

**Code Generation Enhancements:**
- ✅ UUID-based variable names using MD5 hashes instead of timestamps
- ✅ Animation objects now named with target object name (e.g., `circle_fadein_abc123`)
- ✅ Added execution order comments to generated code
- ✅ Fixed camera nodes to work in Sequence nodes with proper animation handling
- ✅ Added `order` parameter to all camera nodes for execution control

**New Features:**
- ✅ Created **AnimationGroup** node for parallel animation playback
- ✅ Updated Property Inspector to show all schema properties (including new fields)
- ✅ Fixed camera animation timing (instant vs animated based on run_time)

**Documentation:**
- ✅ Added comprehensive code review findings to TODO.md
- ✅ Documented project scope (personal use, no public deployment planned)

### Summary

Completed major performance optimizations, code quality improvements, and enhanced code generation to produce more readable output with better variable naming and execution tracking. Added AnimationGroup node for parallel animations and fixed camera node integration with sequences.

## 2026-02-10 14:55

**Branch:** Not a git repository

### Completed
- Enhanced code generator with improved MANIM code generation logic (backend/core/code_generator.py)
- Extended animation nodes with new animation types (backend/nodes/animations.py)
- Added camera control nodes for scene manipulation (backend/nodes/camera.py)
- Improved graph validation and logging configuration
- Built frontend production bundle (dist/)
- Updated type definitions for syntax highlighting support
- Completed export dialog UI with quality and FPS selection
- Implemented drag-and-drop JSON file loading on canvas
- Added edge highlighting in blue for selected edges
- Fixed parameter placeholder replacement for pivot, target, and angle_rad

### In Progress
- Frontend build artifacts and pytest cache indicate recent testing/build activity
- Node system expansion with camera and animation capabilities

### Blockers
- None

### Next Steps
- Consider implementing keyboard shortcuts (Ctrl+S, Delete, Esc)
- Add visual error highlighting on nodes when validation fails
- Evaluate exposing node parameters as optional input connectors
- Plan security review before production deployment (code injection, CORS, rate limiting)

## Session Wrap-up - 2026-02-10

**Date:** 2026-02-10

### What Got Done

- ✅ **Removed all scene node requirements** - Updated 14 nodes across shapes3d.py, math.py, and shapes.py to eliminate scene dependencies (Sphere, Cube, Cone, Cylinder, Torus, Axes3D, Axes, NumberPlane, MathTex, Vector, Dot, Line, Text, Arrow)
- ✅ **Implemented Vec3 comma-separated input** - Converted Vec3 from three separate fields to single string input (e.g., "2, 3, 4")
- ✅ **Added Vec3Split and Vec3Combine nodes** - Created two new utility nodes for splitting Vec3 into x,y,z Numbers and combining them back
- ✅ **Upgraded Matrix to 4x4** - Expanded from 3x3 to 4x4 (16 fields) with grid display in UI
- ✅ **Fixed multi-output node handling in code generator** - Major fix to properly handle nodes with multiple outputs by tracking source handles and appending suffixes to variable names
- ✅ **End-to-end testing** - Verified all features with code generation and MANIM rendering

### Summary

Completed major architectural improvements to manim-nodes by removing scene dependencies system-wide, implementing comma-separated Vec3 input, adding split/combine utilities, upgrading Matrix to 4x4, and fixing critical code generator bug for multi-output nodes. All 50 nodes now work without scene requirements, and the system successfully generates and renders animations end-to-end.

## 2026-02-10 (latest check-in)

**Branch:** Not a git repository

### Completed
- No new commits beyond previous session wrap-up

### In Progress
- Frontend production build generated (`frontend/dist/`)
- Pytest cache present from recent test runs (root and frontend)
- Core frontend components are stable with full feature set:
  - ConnectionMenu: Type-aware node creation from dangling connections
  - CustomNode: Category-based styling, collapsible params, summary info, shaped handles
  - NodeEditor: Drag-and-drop JSON import, connection menu integration
  - CodeViewer: Syntax-highlighted viewer with copy/download
  - Inspector: Schema-driven editing with matrix grid, enums, color pickers
  - useGraphStore: Auto edge replacement on same target handle

### Blockers
- None

### Next Steps
- Implement keyboard shortcuts (Ctrl+S save, Delete node, Esc deselect)
- Add visual error highlighting on nodes when validation fails
- Evaluate exposing node parameters as optional input connectors
- Address security items from code review (input sanitization, CORS, rate limiting)

## 2026-02-11

**Branch:** main

### Completed
- Initial git commit of full manim-nodes project including:
  - FastAPI backend (REST API, WebSocket, node system, code generation, MANIM rendering)
  - React 18 + TypeScript frontend (React Flow editor, Zustand state, TailwindCSS)
  - Docker Compose deployment configuration
  - Project documentation (CLAUDE.md, QUICKSTART_TEST.md)

### In Progress
- None (clean working tree)

### Blockers
- None

### Next Steps
- Verify end-to-end workflow (create graph → render preview → view animation)
- Add unit tests for backend core modules (validation, code generation)
- Expand node type library (shapes, animations, math)

## Session Wrap-up - 2026-02-11

**Date:** 2026-02-11

### What Got Done

- ✅ **16 new math operation nodes** registered in NODE_REGISTRY (Negate, Vec3Add/Subtract/Scale/Negate/Dot/Cross/Length/Normalize, MatrixAdd/Subtract/Inverse/Transpose/Negate/Determinant/VecMultiply)
- ✅ **Fixed Graph validation error** — made `id` field optional so render requests don't fail
- ✅ **DisplayMatrix decimal formatting** — limited to 3 decimal places
- ✅ **ComposeMatrix intuitive ordering** — reversed multiplication so m1 applies first (user-friendly order)
- ✅ **Fixed `about_point="self"`** — now uses `mob.get_center()` at runtime, respecting prior MoveTo animations
- ✅ **Created TransformInPlace node** — combines Scale, Rotation, Translation, and target position in one node with `copy` flag support; multiple iterations based on user feedback
- ✅ **Rewrote Pythagorean Theorem example** with TransformInPlace nodes (reduced from 18 nodes to 6 per arrangement)
- ✅ **Added a²+b² rearrangement** to Pythagorean example — second (a+b)² frame showing triangles arranged to leave a² and b² squares, completing the full visual proof
- ✅ **Camera zoom** — added PythonCode node injecting `self.set_camera_orientation(zoom=0.75)` for wider view
- ✅ **Title and layout adjustments** — added title text, shifted proof frames down, adjusted all coordinates to prevent overlapping
- ✅ **Side-length labels** — added a/b labels on the a²+b² arrangement
- ✅ **Documented the example build process** — created `backend/examples/PYTHAGOREAN_EXAMPLE.md` covering geometry derivations, node structure, animation phases, and key techniques

### Summary

Major session focused on the TransformInPlace node and the Pythagorean Theorem rearrangement proof example. Created a powerful new animation node that combines scale, rotation, translation, and target positioning in one step with copy support. Built a comprehensive 38-node, 10-phase animated proof showing both the c² and a²+b² arrangements side by side, with full documentation of the geometric reasoning and build process.

## 2026-02-11 (session 2)

**Branch:** main

### Completed
- Added 16 new math operation nodes: Negate, Vec3 arithmetic (Add/Subtract/Scale/Negate/Dot/Cross/Length/Normalize), Matrix operations (Add/Subtract/Inverse/Transpose/Negate/Determinant/VecMultiply)
- Added new utility nodes: DebugPrint, PythonCode, TransformInPlace, ExtractEdges, ExposeParameters
- Added `copy` flag to animation nodes (FadeIn, FadeOut, Show, Write, Create, Morph, Rotate, Scale) to animate copies while preserving originals
- Renamed transform animations for clarity (ReplacementTransform → ReplacementMorph, TransformFromCopy → MorphFromCopy, etc.)
- Added SquareFromEdge, LineLabel, and ParametricFunction nodes
- Expanded Group and Sequence/AnimationGroup slots from 5 to 10 inputs
- Changed `about_point` default from "center" to "self" (uses mob.get_center() at runtime)
- Major code generator improvements: deferred label support, pending shape labels, upstream chain animation playback
- Built examples system: backend API (`/examples` endpoint), frontend examples browser in TopBar
- Created Pythagorean Theorem proof example with documentation
- Made graph `id` field optional to fix render request validation
- Enhanced CustomNode: dynamic handle management for ExposeParameters, inline animate/copy toggles, tall node layout

### In Progress
- 18 files modified, ~1,550 lines added across backend and frontend (uncommitted)
- New files: `backend/api/examples.py`, `backend/examples/` directory

### Blockers
- None

### Next Steps
- Commit current batch of changes
- Add more example graphs to the examples library
- Implement keyboard shortcuts (Ctrl+S, Delete, Esc)
- Address remaining security items from code review

## 2026-02-12 10:00

**Branch:** main

### Completed
- Expanded animation node library with 20+ new types: creation (Uncreate, Unwrite, DrawBorderThenFill, SpiralIn), growing (GrowFromCenter/Point/Edge, GrowArrow, SpinInFromNothing), indication (Indicate, Flash, Circumscribe, Wiggle, ApplyWave, FocusOn), transform (FadeMorph, MorphMatchingShapes, FadeToColor)
- Added new shape nodes: RightTriangle, IsoscelesTriangle, RegularPolygon, LineLabel
- Implemented full vector/matrix math operations suite (Vec3Add/Cross/Dot, MatrixMultiply/Inverse/Transform)
- Added FunctionDef/FunctionCall and PythonCode utility nodes for code injection
- Overhauled code generator: junction resolution, variable deduplication, multi-output handling, `var_to_node_id` error tracking (~480 lines added)
- Implemented error node identification: backend maps MANIM errors to specific node IDs, frontend highlights offending nodes with red borders
- Built Group Frames (GroupFrameNode): visual-only container nodes with drag-to-attach, resize, and editable titles
- Added Debug Panel: bottom panel with render logs and auto-scrolling log viewer
- Implemented edge cutting with Shift+drag (line segment intersection detection)
- Added drag-and-drop .json graph file import onto canvas
- Enhanced handle styling per data type: blue circles (Mobject), purple triangles (Animation), teal diamonds (Number), teal triangles (Vec3), pink circles (Color)
- Added viewport persistence (saves/restores zoom/pan per graph)
- Added node duplication support
- Added `html-to-image` dependency (graph export/screenshot)
- Enhanced graph validator: frame node support, flexible optional input rules, better error messages
- Added `/api/graphs/{id}/objects` endpoint for cross-graph object listing

### In Progress
- 32 files modified + 2 new files across backend and frontend (uncommitted on main)

### Blockers
- None

### Next Steps
- Commit current batch of changes
- Test new animation nodes end-to-end with MANIM rendering
- Add example graphs showcasing new animation types (indication, growing)
- Keyboard shortcuts (Ctrl+S save, Delete node, Esc deselect)
- Address remaining security items (input sanitization, CORS, rate limiting)

## Session Wrap-up - 2026-02-12

**Date:** 2026-02-12

### What Got Done

**New Examples:**
- Built **2D Parametric Curves** example with NumberPlane, ZoomCamera, two ParametricFunction curves (t sin 2t, cos(t-pi)-t), Dots with MoveAlongPath, and AnimationGroup
- Built **3D Parametric Curves** example extending the 2D version with Axes3D, NumberPlane, and SetCameraOrientation
- Built **Lorenz Attractor** example with Euler-integrated Lorenz system cached on numpy, live-plotted with Write presentation, dual camera orientations for rotation effect
- Organized all parametric/Lorenz examples with `__groupFrame` nodes for visual clarity

**Group Frame Fixes:**
- Fixed nodes unable to detach from frames by removing `extent: 'parent'` constraint across 5 frontend files and all backend examples
- Fixed frame resize handle grabbing the frame instead of resizing (added `nodrag` CSS class)
- Added 15px grid snapping to frame resize logic

**README & Documentation:**
- Rewrote README with accurate feature list (122 node types), full node type table, architecture diagram, and data flow explanation
- Created `scripts/export_example_gifs.py` to render all 6 examples as palette-optimized GIFs via manim + ffmpeg
- Successfully exported all 6 example GIFs (basic_shapes, pythagorean, parametric2d, parametric3d, lorenz, sqrt2) into `docs/examples/`
- Renamed parametric examples from "fourier" to "parametric2d"/"parametric3d" across IDs, filenames, and README references

### Summary

Built three new example graphs (2D/3D parametric curves, Lorenz attractor), fixed multiple group frame UX issues (detach, resize, snap), and created a complete README with GIF previews of all 6 built-in examples exported via an automated rendering pipeline.
