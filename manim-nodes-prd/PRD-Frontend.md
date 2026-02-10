# PRD: Frontend Requirements

> Project: manim-nodes
> Generated: 2026-02-07
> Status: Draft

## Overview

This document specifies the frontend (React + TypeScript) requirements for manim-nodes, including UI components, state management, interactions, and user experience.

---

## Technology Stack

### Core Technologies

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| **Framework** | React | 18+ | Industry standard, large ecosystem |
| **Language** | TypeScript | 5.0+ | Type safety, better DX |
| **Build Tool** | Vite | 5.0+ | Fast dev server, modern bundler |
| **Package Manager** | npm or pnpm | Latest | Dependency management |

### UI & Styling

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Node Graph Library** | React Flow | Node-based visual programming interface |
| **UI Components** | Radix UI or shadcn/ui | Accessible, headless components |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Icons** | Lucide React or Heroicons | Icon library |

### State Management

| Layer | Technology | Purpose |
|-------|------------|---------|
| **UI State** | Zustand | Lightweight global state (selected nodes, UI mode, etc.) |
| **Server State** | TanStack Query (optional, future) | API caching, refetching (if needed) |
| **Form State** | React Hook Form (optional) | Form handling (if complex forms needed) |

### Real-Time Communication

| Component | Technology | Purpose |
|-----------|------------|---------|
| **WebSocket Client** | reconnecting-websocket or Socket.IO | Auto-reconnection, robust connection management |

---

## Application Structure

### Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── NodeEditor/
│   │   │   ├── NodeEditor.tsx         # Main graph editor
│   │   │   ├── NodePalette.tsx        # Left sidebar (node library)
│   │   │   ├── CustomNode.tsx         # React Flow custom node component
│   │   │   └── ConnectionLine.tsx     # Custom connection styling
│   │   ├── AnimationPreview/
│   │   │   ├── Preview.tsx            # Right panel (video player)
│   │   │   ├── PlaybackControls.tsx   # Play/pause/scrub
│   │   │   └── Timeline.tsx           # Animation timeline
│   │   ├── PropertyInspector/
│   │   │   ├── Inspector.tsx          # Property editor panel
│   │   │   ├── NumberInput.tsx        # Custom input components
│   │   │   ├── ColorPicker.tsx
│   │   │   └── ...
│   │   ├── TopBar/
│   │   │   ├── TopBar.tsx             # File/Edit/View menus
│   │   │   ├── SaveButton.tsx
│   │   │   └── ExportButton.tsx
│   │   └── ui/                        # shadcn/ui components
│   │       ├── button.tsx
│   │       ├── dialog.tsx
│   │       └── ...
│   ├── store/
│   │   ├── useGraphStore.ts           # Zustand store (graph state)
│   │   ├── useUIStore.ts              # UI state (selected nodes, mode)
│   │   └── usePreviewStore.ts         # Preview state (playback, frames)
│   ├── api/
│   │   ├── client.ts                  # Axios or Fetch wrapper
│   │   ├── graphs.ts                  # Graph CRUD endpoints
│   │   ├── templates.ts               # Template endpoints
│   │   └── export.ts                  # Export endpoints
│   ├── websocket/
│   │   ├── PreviewWebSocket.ts        # WebSocket connection manager
│   │   └── usePreviewSocket.tsx       # React hook for WebSocket
│   ├── types/
│   │   ├── graph.ts                   # Graph, Node, Edge types
│   │   ├── api.ts                     # API request/response types
│   │   └── preview.ts                 # Preview-related types
│   ├── utils/
│   │   ├── graphValidator.ts          # Client-side validation
│   │   ├── nodeDefinitions.ts         # Node type definitions
│   │   └── shortcuts.ts               # Keyboard shortcut handlers
│   ├── App.tsx                        # Root component
│   ├── main.tsx                       # Entry point
│   └── index.css                      # Global styles + Tailwind imports
├── public/
│   └── ...
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## Core Components

### 1. NodeEditor (Main Graph Canvas)

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| REQ-FE-001 | React Flow Integration | Use React Flow for node graph rendering | Must |
| REQ-FE-002 | Drag-and-Drop | Drag nodes from palette to canvas | Must |
| REQ-FE-003 | Node Selection | Click to select, Ctrl+click for multi-select | Must |
| REQ-FE-004 | Connection Creation | Drag from output port to input port | Must |
| REQ-FE-005 | Pan & Zoom | Middle-mouse drag, mouse wheel zoom | Must |
| REQ-FE-006 | Auto-Layout | Right-click menu → "Auto-arrange nodes" | Should |
| REQ-FE-007 | Grid Snap (Optional) | Snap nodes to grid for alignment | Could |

**React Flow Configuration:**
- **Node Types:** Custom components for each node type (Circle, FadeIn, etc.)
- **Edge Types:** Custom connection lines (colored by data type)
- **Controls:** Minimap (optional), zoom controls, fit-view button

**Custom Node Component:**
```tsx
// components/NodeEditor/CustomNode.tsx
interface CustomNodeProps {
  id: string;
  data: {
    label: string;
    type: string;
    inputs: Record<string, any>;
    outputs: Record<string, any>;
    error?: string;
  };
}

function CustomNode({ id, data }: CustomNodeProps) {
  return (
    <div className={`custom-node ${data.error ? 'error' : ''}`}>
      <div className="node-header">{data.label}</div>
      <div className="node-inputs">
        {/* Render input handles */}
      </div>
      <div className="node-outputs">
        {/* Render output handles */}
      </div>
      {data.error && <div className="error-badge">⚠</div>}
    </div>
  );
}
```

---

### 2. NodePalette (Left Sidebar)

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| REQ-FE-008 | Categorized Node List | Nodes grouped by category (Shapes, Animations, etc.) | Must |
| REQ-FE-009 | Search Bar | Fuzzy search for node names | Must |
| REQ-FE-010 | Drag to Canvas | Drag node from palette to editor | Must |
| REQ-FE-011 | Node Preview (Optional) | Show icon/thumbnail for each node | Could |

**Categories:**
- Shapes (Circle, Square, Line, etc.)
- Animations (FadeIn, Move, Transform, etc.)
- Math (Axes, Graph, Vector, etc.)
- Colors & Styles (SetColor, SetOpacity, etc.)
- Logic (Conditional, Loop, etc.)
- Utilities (Timer, Variable, etc.)

**Search Implementation:**
- Use Fuse.js for fuzzy search
- Search by node name, category, tags
- Keyboard shortcut: `Ctrl+K` to focus search

---

### 3. AnimationPreview (Right Panel)

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| REQ-FE-012 | Video Player | Display animation frames as video | Must |
| REQ-FE-013 | Playback Controls | Play, pause, stop, scrub timeline | Must |
| REQ-FE-014 | Speed Control | Adjust playback speed (0.5x, 1x, 2x, 4x) | Must |
| REQ-FE-015 | Loop Toggle | Repeat animation continuously | Must |
| REQ-FE-016 | Fullscreen | Maximize preview for presentations | Should |
| REQ-FE-017 | Loading Indicator | Show spinner during render | Must |

**Preview Rendering:**
- WebSocket receives frame URLs from backend
- Load frames as images, display in sequence
- Cache frames for smooth playback
- Fallback to static image if rendering fails

**Playback Controls:**
```tsx
<PlaybackControls>
  <PlayButton onClick={handlePlay} />
  <PauseButton onClick={handlePause} />
  <Timeline currentTime={time} duration={duration} onSeek={handleSeek} />
  <SpeedSelector speeds={[0.5, 1, 2, 4]} onChange={setSpeed} />
  <LoopToggle checked={loop} onChange={setLoop} />
  <FullscreenButton onClick={toggleFullscreen} />
</PlaybackControls>
```

---

### 4. PropertyInspector (Bottom/Right Panel)

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| REQ-FE-018 | Show Selected Node Properties | Display editable parameters when node selected | Must |
| REQ-FE-019 | Input Components | Number, color, text, dropdown, checkbox inputs | Must |
| REQ-FE-020 | Real-Time Updates | Changes apply immediately (debounced preview refresh) | Must |
| REQ-FE-021 | Validation | Show errors for invalid values (red border, tooltip) | Must |
| REQ-FE-022 | Multi-Node Editing (Future) | Edit shared properties of multiple selected nodes | Could |

**Property Types:**
- **Number:** Slider + input field (with min/max)
- **Color:** Color picker (hex input + visual picker)
- **Text:** Text input
- **Dropdown:** Select from options
- **Boolean:** Checkbox or toggle

**Example Property Editor:**
```tsx
// For Circle node
<PropertyInspector node={selectedNode}>
  <NumberInput
    label="Radius"
    value={node.data.radius}
    min={0.1}
    max={10}
    step={0.1}
    onChange={(val) => updateNode(node.id, { radius: val })}
  />
  <ColorPicker
    label="Color"
    value={node.data.color}
    onChange={(val) => updateNode(node.id, { color: val })}
  />
</PropertyInspector>
```

---

### 5. TopBar (File/Edit/View Menus)

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| REQ-FE-023 | File Menu | New, Open, Save, Save As, Export | Must |
| REQ-FE-024 | Edit Menu | Undo, Redo, Cut, Copy, Paste, Delete | Should |
| REQ-FE-025 | View Menu | Zoom In/Out, Fit View, Toggle Panels | Should |
| REQ-FE-026 | Help Menu | Documentation, Keyboard Shortcuts, About | Could |

**File Operations:**
- **New:** Clear canvas, prompt to save if unsaved changes
- **Open:** Show dialog to select saved graph
- **Save:** Update existing graph (or Save As if new)
- **Save As:** Prompt for new name, create copy
- **Export:** Open export dialog (format, quality settings)

---

## State Management

### Zustand Stores

#### 1. Graph Store (`useGraphStore`)

```typescript
// store/useGraphStore.ts
interface GraphStore {
  // Graph data
  graph: Graph | null;
  nodes: Node[];
  edges: Edge[];

  // Actions
  setGraph: (graph: Graph) => void;
  addNode: (node: Node) => void;
  updateNode: (id: string, data: Partial<Node>) => void;
  deleteNode: (id: string) => void;
  addEdge: (edge: Edge) => void;
  deleteEdge: (id: string) => void;
  clear: () => void;

  // Dirty state
  isDirty: boolean;
  markDirty: () => void;
  markClean: () => void;
}
```

#### 2. UI Store (`useUIStore`)

```typescript
// store/useUIStore.ts
interface UIStore {
  // Selected nodes
  selectedNodes: string[];
  setSelectedNodes: (ids: string[]) => void;

  // UI mode
  mode: 'edit' | 'presentation';
  setMode: (mode: 'edit' | 'presentation') => void;

  // Panel visibility
  showPalette: boolean;
  showInspector: boolean;
  togglePalette: () => void;
  toggleInspector: () => void;
}
```

#### 3. Preview Store (`usePreviewStore`)

```typescript
// store/usePreviewStore.ts
interface PreviewStore {
  // Playback state
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  frames: string[];  // Frame URLs

  // Actions
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
  setFrames: (frames: string[]) => void;

  // Loading state
  isRendering: boolean;
  renderProgress: number;
  renderError: string | null;
}
```

---

## Data Persistence

### Auto-Save Strategy

| ID | Feature | Specification | Priority |
|----|---------|---------------|----------|
| REQ-FE-027 | Debounced Auto-Save | Save to backend 2 seconds after last edit | Must |
| REQ-FE-028 | Manual Save Button | User can force save immediately | Must |
| REQ-FE-029 | LocalStorage Cache | Save graph to localStorage on every change | Must |
| REQ-FE-030 | Dirty State Indicator | Show asterisk (*) in title if unsaved changes | Must |

**Auto-Save Flow:**
1. User edits node property
2. Start 2-second timer
3. If another edit occurs → reset timer
4. When timer expires → `PUT /api/graphs/{id}`
5. On success → mark clean, update localStorage
6. On failure → show error toast, keep dirty state

**LocalStorage Backup:**
- Key: `manim-nodes-graph-{id}`
- Value: Serialized graph JSON
- Purpose: Survive page refresh, recover from crashes
- Restore on page load if backend graph is older

---

## WebSocket Integration

### Preview WebSocket

**Connection Management:**
```typescript
// websocket/usePreviewSocket.tsx
function usePreviewSocket() {
  const [socket, setSocket] = useState<ReconnectingWebSocket | null>(null);
  const { setFrames, setRenderProgress } = usePreviewStore();

  useEffect(() => {
    const ws = new ReconnectingWebSocket('ws://localhost:8000/ws/preview');

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'frame') {
        setFrames((prev) => [...prev, msg.url]);
      } else if (msg.type === 'status') {
        setRenderProgress(msg.progress);
      }
    };

    setSocket(ws);
    return () => ws.close();
  }, []);

  const sendRenderRequest = (graph: Graph, quality: string) => {
    socket?.send(JSON.stringify({ type: 'render', graph, quality }));
  };

  return { sendRenderRequest };
}
```

**Reconnection Logic:**
- Use `reconnecting-websocket` library
- Auto-reconnect on connection loss (exponential backoff)
- Show connection status indicator in UI
- Queue messages if disconnected, send on reconnect

---

## Keyboard Shortcuts

### MVP Shortcuts

| Shortcut | Action | Priority |
|----------|--------|----------|
| `Ctrl/Cmd + S` | Save graph | Must |
| `Ctrl/Cmd + Z` | Undo | Must |
| `Ctrl/Cmd + Shift + Z` | Redo | Must |
| `Delete` / `Backspace` | Delete selected node(s) | Must |
| `Ctrl/Cmd + C` | Copy selected node(s) | Should |
| `Ctrl/Cmd + V` | Paste copied node(s) | Should |
| `Ctrl/Cmd + A` | Select all nodes | Should |
| `Ctrl/Cmd + K` | Focus search bar | Should |
| `Space` | Toggle play/pause | Should |
| `Esc` | Deselect all nodes | Should |
| `F11` | Toggle fullscreen preview | Could |

**Implementation:**
```typescript
// utils/shortcuts.ts
import { useEffect } from 'react';

function useKeyboardShortcuts() {
  const { saveGraph, undo, redo, deleteNodes } = useGraphStore();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveGraph();
      } else if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
        e.preventDefault();
        if (e.shiftKey) redo();
        else undo();
      } else if (e.key === 'Delete' || e.key === 'Backspace') {
        deleteNodes();
      }
      // ... more shortcuts
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
}
```

---

## Styling & Theming

### Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',  // Enable dark mode
  theme: {
    extend: {
      colors: {
        background: '#1E1E1E',
        panel: '#252526',
        accent: '#007ACC',
        success: '#4EC9B0',
        warning: '#FFC107',
        error: '#F44336',
        textPrimary: '#D4D4D4',
        textSecondary: '#858585',
      },
    },
  },
};
```

### Component Styling Example

```tsx
// components/NodeEditor/CustomNode.tsx
<div className="
  bg-panel border-2 border-textSecondary
  rounded-lg p-4 min-w-[150px]
  hover:border-accent transition-colors
  data-[error=true]:border-error
">
  <div className="text-textPrimary font-semibold mb-2">{data.label}</div>
  {/* ... */}
</div>
```

---

## Performance Optimization

### React Performance

| Technique | Purpose | Priority |
|-----------|---------|----------|
| `React.memo` | Prevent unnecessary re-renders (node components) | Should |
| `useMemo` / `useCallback` | Memoize expensive computations | Should |
| Virtualization (react-window) | Render large node lists efficiently | Could |
| Code Splitting (lazy loading) | Reduce initial bundle size | Should |

### React Flow Optimization

| Technique | Purpose |
|-----------|---------|
| `nodesDraggable={false}` during render | Prevent interactions during preview updates |
| Debounce graph updates | Batch multiple changes before re-render |
| Limit node/edge count | Warn if graph exceeds 200 nodes |

---

## Error Handling

### Error States

| Error Type | UI Feedback | Priority |
|------------|-------------|----------|
| **Network Error** | Toast notification: "Connection lost. Retrying..." | Must |
| **Validation Error** | Highlight node in red, show error tooltip | Must |
| **Render Failure** | Display error message in preview panel | Must |
| **Save Failure** | Toast notification: "Save failed. Retrying..." | Must |

### Error Boundaries

```tsx
// components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Frontend error:', error, errorInfo);
    // Show error UI, offer to reload or restore from localStorage
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

---

## Browser Compatibility

### Supported Browsers

| Browser | Minimum Version | Notes |
|---------|-----------------|-------|
| Chrome | 90+ | Primary target |
| Firefox | 88+ | Full support |
| Safari | 14+ | WebGL 2.0 required |
| Edge | 90+ | Chromium-based |

### Polyfills (if needed)

- **ResizeObserver:** For responsive panels
- **IntersectionObserver:** For lazy loading

---

## Assumptions

- Users have modern browsers with WebGL 2.0 and WebSocket support
- Internet connection required for initial load (offline after PWA caching, future)
- JavaScript enabled (no fallback)
- Screen resolution ≥ 1366x768

---

## Dependencies

### Critical Dependencies

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| React Flow | Node graph editor | **None** - critical |
| Zustand | State management | Redux (more complex) |
| Tailwind CSS | Styling | CSS Modules (more boilerplate) |

### Optional Dependencies

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| Radix UI / shadcn/ui | UI components | Custom components (more dev time) |
| reconnecting-websocket | WebSocket reliability | Native WebSocket (manual reconnection) |

---

## Open Questions

- [ ] Should frontend support graph templates stored locally (IndexedDB)?
- [ ] Should there be an undo/redo limit (e.g., 50 actions)?
- [ ] Should copy/paste support cross-session (clipboard API)?
- [ ] Should frontend validate graph before sending to backend (duplicate validation)?

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| React Flow performance degrades with large graphs | **Medium** | Limit node count, optimize rendering, virtualization |
| WebSocket disconnects during rendering | **Medium** | Auto-reconnect, resume from last frame |
| LocalStorage quota exceeded | **Low** | Compress graph JSON, clean old backups |
| Browser compatibility issues | **Low** | Test on all supported browsers, polyfills |
