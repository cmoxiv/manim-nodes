# PRD: User Experience

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document defines the user experience requirements for manim-nodes, focusing on the web interface, interaction patterns, and visual design.

## Platform Support

### Target Platforms

| ID | Platform | Priority | Notes |
|----|----------|----------|-------|
| REQ-UX-001 | Desktop Web (Chrome, Firefox, Safari, Edge) | Must | Primary platform - optimized for large screens (1920x1080+) |
| REQ-UX-002 | Laptop Web (1366x768 minimum) | Must | Support common laptop resolutions |
| REQ-UX-003 | Tablet (Future) | Could | Post-MVP: Touch-optimized interface for iPad |
| REQ-UX-004 | Mobile (Future) | Won't | Not practical for complex node editing |

### Browser Requirements

| Requirement | Specification |
|-------------|---------------|
| **Minimum Versions** | Chrome 90+, Firefox 88+, Safari 14+, Edge 90+ |
| **Required Features** | WebGL 2.0, WebSocket, ES6+ JavaScript |
| **Screen Resolution** | Minimum 1366x768, recommended 1920x1080 or higher |

---

## UI Layout & Structure

### Main Editor Layout

**Three-Panel Design:** Node Palette (left) + Graph Editor (center) + Animation Preview (right)

| ID | Panel | Description | Priority |
|----|-------|-------------|----------|
| REQ-UX-005 | Node Palette (Left) | Categorized library of available nodes | Must |
| REQ-UX-006 | Graph Editor (Center) | Main canvas for building node graphs | Must |
| REQ-UX-007 | Animation Preview (Right) | Real-time animation visualization | Must |
| REQ-UX-008 | Property Inspector (Bottom/Right) | Edits selected node parameters | Must |
| REQ-UX-009 | Top Toolbar | File operations, export, settings | Must |

### Layout Specifications

```
┌─────────────────────────────────────────────────────────────────┐
│  [File] [Edit] [View] [Help]          [Save] [Export] [Run]    │
├─────────┬───────────────────────────────────────┬───────────────┤
│         │                                       │               │
│  Node   │                                       │   Animation   │
│ Palette │         Graph Editor Canvas          │    Preview    │
│         │                                       │               │
│ Search: │                                       │   [Play ▶]    │
│ [____]  │   [Node connections and graph]       │   [Pause ⏸]   │
│         │                                       │   Timeline    │
│ Shape   │                                       │   [=========] │
│ ├Circle │                                       │               │
│ ├Square │                                       │   Duration:   │
│ └Line   │                                       │   5.0s        │
│         │                                       │               │
│ Animate │                                       │               │
│ ├FadeIn │                                       │               │
│ ├Move   ├───────────────────────────────────────┤               │
│ └Scale  │   Property Inspector (Selected Node) │               │
│         │   Name: Circle                        │               │
│ Math    │   Radius: [2.5]  Color: [Blue ▼]     │               │
│ ├Axes   │   Position: X[0] Y[0] Z[0]           │               │
│ ├Graph  │                                       │               │
│ └Vector └───────────────────────────────────────┴───────────────┘
```

### Panel Sizing

| Panel | Default Width | Resizable | Collapsible |
|-------|---------------|-----------|-------------|
| Node Palette | 250px | Yes (150-400px) | Yes |
| Graph Editor | Flexible (remaining space) | - | No |
| Animation Preview | 400px | Yes (300-600px) | No |
| Property Inspector | Full width at bottom OR 300px right | Yes | Yes |

---

## Navigation & Interaction Patterns

### Node Discovery & Addition

| ID | Method | Description | Priority | Keyboard Shortcut |
|----|--------|-------------|----------|-------------------|
| REQ-UX-010 | Node Palette Sidebar | Browse categorized nodes, drag to canvas | Must | - |
| REQ-UX-011 | Search Bar | Fuzzy search for node names | Must | Ctrl/Cmd + K |
| REQ-UX-012 | Right-Click Context Menu | Add node at cursor position | Must | Right-click on canvas |
| REQ-UX-013 | Keyboard Shortcuts | Quick access to common nodes | Should | Ctrl/Cmd + Space (opens menu) |

### Node Categories (Palette Organization)

1. **Shapes** - Circle, Square, Rectangle, Line, Polygon, Arrow, Text
2. **Animations** - FadeIn, FadeOut, Write, Unwrite, Transform, Move, Rotate, Scale
3. **Math** - Axes, Graph, Vector, MathTex, NumberPlane
4. **Colors & Styles** - SetColor, SetOpacity, SetStroke, SetFill
5. **Logic** - Conditional, Loop, Sequence, Parallel
6. **Utilities** - Timer, Variable, Math Operations
7. **ML/Data** (Future) - Neural Network, Matrix, Gradient, Plot

### Graph Editor Interactions

| Action | Interaction | Description |
|--------|-------------|-------------|
| **Add Node** | Drag from palette OR right-click menu | Place node on canvas |
| **Select Node** | Left-click | Highlight node, show properties |
| **Move Node** | Click-and-drag | Reposition on canvas |
| **Delete Node** | Select + Delete key OR backspace | Remove from graph |
| **Connect Nodes** | Drag from output port to input port | Create connection wire |
| **Disconnect Wire** | Click wire + Delete OR drag end off port | Remove connection |
| **Multi-Select** | Ctrl/Cmd + click OR drag-select box | Select multiple nodes |
| **Pan Canvas** | Middle-mouse drag OR spacebar + drag | Move viewport |
| **Zoom** | Mouse wheel OR Ctrl/Cmd + +/- | Zoom in/out |
| **Auto-Layout** | Right-click > "Auto-arrange" | Organize graph automatically |

### Animation Preview Interactions

| Action | Interaction | Description |
|--------|-------------|-------------|
| **Play/Pause** | Click play button OR spacebar | Start/stop animation |
| **Scrub Timeline** | Drag timeline slider | Jump to specific frame |
| **Adjust Speed** | Speed dropdown (0.5x, 1x, 2x, 4x) | Control playback speed |
| **Loop Toggle** | Loop button | Repeat animation continuously |
| **Fullscreen** | Fullscreen button OR F11 | Maximize preview |
| **Export** | Export button | Render final video |

---

## User Flows

### Flow 1: Create Animation from Scratch

```
1. Launch manim-nodes (navigate to http://localhost:XXXX)
2. See blank graph editor with node palette on left
3. Search for "Circle" in palette search bar
4. Drag Circle node to canvas
5. Click Circle node → Property inspector shows radius, color, position
6. Set radius = 2.0, color = Blue
7. Search for "FadeIn" in palette
8. Drag FadeIn node to canvas
9. Connect Circle output → FadeIn input (wire appears)
10. Preview auto-updates (debounced) → shows blue circle fading in
11. Click Play button → animation runs
12. Click Export → renders MP4
```

**Target Time:** 5-10 minutes for simple animation

### Flow 2: Use Template

```
1. Launch manim-nodes
2. Click "File" → "Open Template"
3. Browse templates: "Linear Algebra - Matrix Multiplication"
4. Graph loads with pre-built nodes
5. Click matrix node → edit values in property inspector
6. Preview auto-updates with new values
7. Export animation
```

**Target Time:** 2-5 minutes

### Flow 3: Step-by-Step Execution (Teaching)

```
1. Launch manim-nodes with pre-built graph
2. Click "View" → "Presentation Mode" (fullscreen preview, hide editor)
3. Click "Step" button → executes first node only
4. Explain to students what this node does
5. Click "Step" again → executes next node
6. Preview updates incrementally
7. Continue until full animation is built
```

---

## Visual Design

### Design Style

| Aspect | Specification |
|--------|---------------|
| **Overall Style** | Technical/professional (IDE-like, similar to VSCode, Blender) |
| **Color Palette** | Dark theme primary (optional light theme post-MVP) |
| **Typography** | Monospace for code/data, sans-serif for UI (e.g., Inter, Roboto) |
| **Iconography** | Material Design Icons or similar professional icon set |
| **Animation** | Subtle UI transitions (avoid distracting motion) |

### Color Scheme (Dark Theme)

| Element | Color | Purpose |
|---------|-------|---------|
| **Background** | #1E1E1E | Main canvas background |
| **Panels** | #252526 | Sidebar and toolbar backgrounds |
| **Accent** | #007ACC | Selected nodes, active connections |
| **Success** | #4EC9B0 | Valid connections, success states |
| **Warning** | #FFC107 | Warnings, missing inputs |
| **Error** | #F44336 | Error states, invalid connections |
| **Text Primary** | #D4D4D4 | Main text |
| **Text Secondary** | #858585 | Labels, secondary text |

### Node Visual Design

```
┌─────────────────┐
│  Circle         │  ← Node title
├─────────────────┤
│ ○ radius        │  ← Input port (left side)
│ ○ color         │
│                 │
│      [icon]     │  ← Node type icon/preview
│                 │
│        shape ○  │  ← Output port (right side)
└─────────────────┘
```

**Node States:**
- **Default:** Gray border, white title
- **Selected:** Blue border (accent color), highlighted
- **Error:** Red border, error icon badge
- **Executing:** Yellow border, loading animation

**Connection Wires:**
- **Valid:** Smooth bezier curve, accent color
- **Invalid:** Dashed line, red color (during drag)
- **Data Type Colors:** Different colors for Shape, Number, String, etc.

---

## Animation Preview Behavior

### Preview Update Strategy

| ID | Strategy | Description | Priority |
|----|----------|-------------|----------|
| REQ-UX-014 | Debounced Auto-Update | Wait 1-2 seconds after last graph change before re-rendering | Must |
| REQ-UX-015 | Manual Refresh Button | User can force immediate refresh if needed | Should |
| REQ-UX-016 | Loading Indicator | Show spinner during render (for slow graphs) | Must |

**Debounce Logic:**
- User edits node property → start 1.5-second timer
- If another edit occurs within 1.5 sec → reset timer
- When timer expires → trigger backend re-render
- Show loading spinner in preview panel during render

### Preview Quality Settings

| Setting | Description | Use Case |
|---------|-------------|----------|
| **Low (480p)** | Fast preview, lower quality | Complex graphs, rapid iteration |
| **Medium (720p)** | Balanced quality/speed | Default preview mode |
| **High (1080p)** | Full quality, slower | Final review before export |

**Note:** Export always uses high quality regardless of preview setting.

---

## Accessibility

### MVP Accessibility (Basic)

| ID | Feature | Priority | Notes |
|----|---------|----------|-------|
| REQ-UX-017 | Keyboard Navigation | Won't (Post-MVP) | Not prioritized for MVP |
| REQ-UX-018 | Screen Reader Support | Won't (Post-MVP) | Complex visual tool, low priority |
| REQ-UX-019 | Color Contrast | Should | Ensure readability for low vision users |
| REQ-UX-020 | Focus Indicators | Should | Visible focus states for interactive elements |

**Post-MVP Roadmap:** WCAG 2.1 Level AA compliance for broader accessibility.

---

## Internationalization

### Language Support

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| REQ-UX-021 | English Only (MVP) | Must | Primary language for initial release |
| REQ-UX-022 | i18n Infrastructure | Could | Prepare codebase for future translations |
| REQ-UX-023 | Multi-Language (Post-MVP) | Could | Spanish, French, Mandarin (based on demand) |

---

## Responsive Design

### Breakpoints

| Breakpoint | Width | Layout Adjustments |
|------------|-------|-------------------|
| **Desktop Large** | > 1920px | Default three-panel layout |
| **Desktop** | 1366-1920px | Default layout, slightly compressed panels |
| **Laptop** | 1024-1366px | Collapsible node palette, focus on editor |
| **Tablet** | 768-1024px | **Not supported in MVP** |
| **Mobile** | < 768px | **Not supported** |

---

## Key Screens & States

### 1. Landing Screen (First Load)
- Welcome message: "Welcome to manim-nodes"
- Quick actions: "New Project" | "Open Template" | "Load Existing"
- Recent projects list (if available)

### 2. Main Editor (Active Editing)
- Three-panel layout as described above
- Graph with nodes and connections
- Live preview updating

### 3. Presentation Mode
- Fullscreen preview only
- Minimal controls (play, pause, step)
- ESC to exit

### 4. Export Dialog
- Format selection (MP4, GIF)
- Quality settings (resolution, frame rate)
- Progress bar during render
- Download button when complete

---

## Performance Requirements

### UI Responsiveness

| Action | Target Response Time | Notes |
|--------|---------------------|-------|
| **Node Addition** | < 100ms | Instant feedback |
| **Property Edit** | < 50ms | Immediate UI update |
| **Preview Update** | < 2 seconds (simple graphs) | After debounce delay |
| **Graph Load** | < 1 second (100-node graph) | From saved file |
| **Canvas Pan/Zoom** | 60fps | Smooth interaction |

### Graph Complexity Limits (MVP)

| Metric | Limit | Notes |
|--------|-------|-------|
| **Max Nodes** | 200 nodes | Performance degrades beyond this |
| **Max Connections** | 500 wires | Visual clarity and performance |
| **Animation Duration** | 60 seconds | Longer animations may be slow |

---

## Assumptions

- Users have modern browsers with WebGL 2.0 support
- Desktop/laptop screens are primary (1366x768 minimum)
- Users are familiar with drag-and-drop interfaces (similar to Blender, Figma, etc.)
- Self-hosted deployment means no mobile access required

## Dependencies

- Node graph rendering library (e.g., React Flow, Rete.js, or custom WebGL)
- Frontend framework (React, Vue, or Svelte)
- WebSocket library for real-time preview updates

## Open Questions

- [ ] Should node palette categories be user-customizable?
- [ ] Should graph editor support minimap (for large graphs)?
- [ ] Should there be a graph history/undo system?
- [ ] Should preview support side-by-side comparison of graph versions?

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Node graph becomes cluttered with large graphs | Medium | Auto-layout, zoom controls, minimap (future) |
| Preview latency frustrates users | High | Optimize backend rendering, debounce updates, quality settings |
| IDE-like design intimidates non-technical users | Medium | User testing with instructors; onboarding tutorials |
