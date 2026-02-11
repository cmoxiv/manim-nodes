# Pythagorean Theorem Example — Build Process

This document walks through how the Pythagorean Theorem rearrangement proof example was built in manim-nodes, from geometric reasoning to final node graph.

---

## 1. The Mathematical Proof

The classic rearrangement proof of **a² + b² = c²** works by constructing two copies of the same **(a+b)²** square and filling each with four identical right triangles (legs a and b, hypotenuse c). The remaining area differs:

| Frame | Triangles arranged as | Remaining area |
|-------|----------------------|----------------|
| **Right (c²)** | Pinwheel around a tilted square | One tilted square with side c → area **c²** |
| **Left (a²+b²)** | Two rectangles (each split by diagonal) | Two axis-aligned squares: side a and side b → area **a² + b²** |

Since both frames have the same total area (a+b)² and contain the same four triangles, the leftover areas must be equal: **a² + b² = c²**.

---

## 2. Choosing Triangle Dimensions

We pick a **3-4-5 family** triangle scaled down for visual balance:

```
a = 1.5   (base, short leg)
b = 2.0   (height, long leg)
c = 2.5   (hypotenuse)
```

The **(a+b)² frame** has side length **3.5**, so half-side = **1.75**.

---

## 3. Scene Layout

With camera zoom = 0.75 the visible area is approximately **19 × 10.7 units**.

```
y
5.3 ┌─────────────────────────────────────┐
    │            "Pythagorean Theorem"     │  ← Title at y=4.5
    │                                     │
    │              △ (source)             │  ← Triangle at (0, 3.0)
    │           with a², b², c²           │     with SquareFromEdge squares
    │           squares on sides          │     and a, b, c side labels
    │                                     │
    │  ┌───────────┐     ┌───────────┐    │
    │  │ a² │      │     │  ╱╲       │    │  ← Both frames centered at y=-1.0
    │  │    │ tri   │     │╱  ╲ c²   │    │     Left: (-3.5, -1.0)
    │  │────│ tri   │     │╲  ╱      │    │     Right: (3.5, -1.0)
    │  │ tri│  b²  │     │  ╲╱       │    │
    │  └───────────┘     └───────────┘    │
    │                                     │
    │          a² + b² = c²               │  ← Equation at y=-3.8
-5.3└─────────────────────────────────────┘
   -9.5                                  9.5
```

---

## 4. Coordinate Geometry

### 4.1 Source Triangle (Manim internals)

`RightTriangle(base=1.5, height=2.0)` creates a `Polygon` with vertices:

```
(0, 0, 0),  (1.5, 0, 0),  (0, 2.0, 0)
```

Manim auto-centers the bounding box, giving vertices relative to center:

```
A = (-0.75, -1.0)   ← right-angle vertex
B = ( 0.75, -1.0)   ← end of base (leg a)
C = (-0.75,  1.0)   ← end of height (leg b)
```

From the right-angle vertex A:
- **Leg a** (1.5) runs along **+x**
- **Leg b** (2.0) runs along **+y**

The bounding box center is **(0, 0)**, so `move_to(position)` places the center at `position`.

### 4.2 Right Frame — c² Arrangement

Frame center: **(3.5, -1.0)**. Corners at ±1.75 from center.

The four triangles form a **pinwheel** around the tilted c² square. Each triangle occupies one corner of the frame. The rotation maps the original triangle's legs to align with the frame edges:

| Triangle | Corner | Rotation | Bounding-box center (target) |
|----------|--------|----------|------------------------------|
| T1 | Bottom-left | 0° | (2.5, -1.75) |
| T2 | Bottom-right | 90° | (4.25, -2.0) |
| T3 | Top-right | 180° | (4.5, -0.25) |
| T4 | Top-left | -90° | (2.75, 0.0) |

**Why these rotations work:**

Take T1 (0°, bottom-left corner BL = (1.75, -2.75)):
- Right-angle A at BL: center + A = target + (-0.75, -1.0)
- Solve: target = (BL_x + 0.75, BL_y + 1.0) = (2.5, -1.75) ✓
- B at (2.5+0.75, -1.75-1.0) = (3.25, -2.75) → on bottom edge ✓
- C at (2.5-0.75, -1.75+1.0) = (1.75, -0.75) → on left edge ✓

For T2 (90° CCW, bottom-right corner BR = (5.25, -2.75)):
- 90° rotation maps: +x → +y, +y → -x
- So leg a goes along +y and leg b goes along -x
- Right angle ends up at BR, legs align with right and bottom edges

The same logic applies for T3 (180°) and T4 (-90°).

**Inner tilted c² square** vertices (relative to frame center):

```
(-0.25, -1.75),  (1.75, -0.25),  (0.25, 1.75),  (-1.75, 0.25)
```

These are the points where the frame edges are divided into segments of length a and b.

### 4.3 Left Frame — a²+b² Arrangement

Frame center: **(-3.5, -1.0)**. Same (a+b)² outer square.

The frame is divided by an internal horizontal line and vertical line into four regions:

```
         a=1.5       b=2.0
       ┌─────────┬───────────┐
       │         │           │
a=1.5  │   a²    │  2 tris   │  ← top-right rectangle (b × a)
       │         │           │
       ├─────────┼───────────┤  ← y-divide at frame_center_y + b - 1.75
       │         │           │
       │ 2 tris  │    b²     │  ← bottom-right square (b × b)
b=2.0  │         │           │
       │         │           │
       └─────────┴───────────┘
         x-divide at frame_center_x + a - 1.75
```

Division lines (absolute coordinates):
- Vertical: x = -3.5 - 1.75 + 1.5 = **-3.75**
- Horizontal: y = -1.0 - 1.75 + 2.0 = **-0.75**

The four triangles fill the two rectangles. Each rectangle's bounding-box center becomes the `target` for the two triangles inside it:

| Triangle | Rectangle | Rotation | Target |
|----------|-----------|----------|--------|
| T-L1 | Bottom-left (a×b) | 0° | (-4.5, -1.75) |
| T-L2 | Bottom-left (a×b) | 180° | (-4.5, -1.75) |
| T-L3 | Top-right (b×a) | 90° | (-2.75, 0.0) |
| T-L4 | Top-right (b×a) | -90° | (-2.75, 0.0) |

**Key insight:** Two triangles in the same rectangle share the **same bounding-box center** (and thus the same `target`). They tile correctly because one fills the upper-left half and the other fills the lower-right half of the rectangle.

**No reflections needed.** All four orientations (0°, 90°, 180°, -90°) are pure rotations. The triangle's chirality naturally matches because:
- 0° and 180° fill the a×b rectangle (legs align with width a and height b)
- 90° and -90° fill the b×a rectangle (legs swap to align with width b and height a)

Remaining squares:
- **a² square** (top-left): center (-4.5, 0.0), half-side 0.75
- **b² square** (bottom-right): center (-2.75, -1.75), half-side 1.0

---

## 5. Node Graph Structure

### 5.1 Node Inventory (38 nodes total)

| Category | Nodes | Count |
|----------|-------|-------|
| Setup | PythonCode (camera zoom), Text (title), Show (title) | 3 |
| Source shape | RightTriangle | 1 |
| Edge squares | SquareFromEdge × 3 | 3 |
| Side labels | LineLabel × 3, Write × 3 | 6 |
| Right arrangement | TransformInPlace × 4 (copy=true) | 4 |
| Right frame | Polyline × 2 (outer + c² inner) | 2 |
| Right overlays | Create, FadeIn, MathTex × 4 (a/b/c/c²), Write × 4 | 9 |
| Left arrangement | TransformInPlace × 4 (copy=true) | 4 |
| Left frame | Polyline × 3 (outer + a² + b²) | 3 |
| Left overlays | Create, FadeIn × 2, MathTex × 4 (a²/b²/a/b), Write × 4 | 11 |
| Equation | MathTex, Write | 2 |
| Grouping | AnimationGroup × 6, Sequence × 1 | 7 |

### 5.2 Key Connections

```
RightTriangle ──shape──→ Create ──────────────────────────→ Sequence (anim1)
      │
      ├──side_1──→ SquareFromEdge(a) ──→ ┐
      ├──side_2──→ SquareFromEdge(c) ──→ ├─ AnimationGroup ──→ Sequence (anim2)
      ├──side_3──→ SquareFromEdge(b) ──→ ┘
      │
      ├──side_1──→ LineLabel(a) → Write ─→ ┐
      ├──side_2──→ LineLabel(c) → Write ─→ ├─ AnimationGroup ──→ Sequence (anim3)
      ├──side_3──→ LineLabel(b) → Write ─→ ┘
      │
      ├──shape──→ TransformInPlace(0°,  copy) ──→ ┐
      ├──shape──→ TransformInPlace(90°, copy) ──→ ├─ AnimGroup ──→ Seq (anim4)
      ├──shape──→ TransformInPlace(180°,copy) ──→ ┤   (c² arrangement)
      ├──shape──→ TransformInPlace(-90°,copy) ──→ ┘
      │
      ├──shape──→ TransformInPlace(0°,  copy) ──→ ┐
      ├──shape──→ TransformInPlace(180°,copy) ──→ ├─ AnimGroup ──→ Seq (anim8)
      ├──shape──→ TransformInPlace(90°, copy) ──→ ┤   (a²+b² arrangement)
      └──shape──→ TransformInPlace(-90°,copy) ──→ ┘
```

---

## 6. Animation Sequence (10 Phases)

| Phase | Seq slot | What happens | Duration |
|-------|----------|-------------|----------|
| 1 | anim1 | Create source triangle at top center | 1.5s |
| 2 | anim2 | Grow a², b², c² squares from triangle edges | 1.5s |
| 3 | anim3 | Write side labels (a, b, c) | 1.0s |
| 4 | anim4 | Arrange 4 copies into c² pinwheel (right) | 1.5s |
| 5 | anim5 | Show right frame + tilted c² square overlay | 1.0s |
| 6 | anim6 | Write proof labels (a, b, c on right frame) | 0.8s |
| 7 | anim7 | Write c² label at center of right frame | 0.8s |
| 8 | anim8 | Arrange 4 copies into a²+b² rectangles (left) | 1.5s |
| 9 | anim9 | Show left frame + a²/b² squares + all labels | 1.2s |
| 10 | anim10 | Write equation **a² + b² = c²** | 1.5s |

Wait time between phases: **0.5s**

---

## 7. Key Techniques Demonstrated

### 7.1 TransformInPlace with `copy=true`

The central technique. One source triangle produces **8 copies** (4 per frame), each with different rotation and target position. Without `copy`, each animation would consume the original.

**Old approach** (before TransformInPlace): 4 RightTriangle nodes + 4 Vec3 + 4 MoveTo + 4 Rotate + 2 AnimationGroups = **18 nodes** per frame.

**New approach**: 1 RightTriangle + 4 TransformInPlace + 1 AnimationGroup = **6 nodes** per frame.

### 7.2 Camera Zoom via PythonCode

A `PythonCode` node injects `self.set_camera_orientation(zoom=0.75)` at the start of the scene, zooming out to fit both frames, the source triangle, title, and equation.

### 7.3 Standalone Show Node

The title uses `Text → Show` without being in the Sequence. Standalone `Show` nodes call `self.add()` immediately, displaying the title before any animated phases begin.

### 7.4 Polyline for Arbitrary Shapes

The tilted c² square and the a²/b² rectangles are drawn with `Polyline` nodes using explicit vertex coordinates (relative to the shape's position). The `closed=true` flag connects the last vertex back to the first.

### 7.5 SquareFromEdge

The `SquareFromEdge` node takes a triangle's side output and grows a square outward from that edge. This automatically handles positioning, rotation, and sizing — the square aligns perpendicular to the edge.

### 7.6 LineLabel

Labels (a, b, c) on the triangle sides use `LineLabel`, which takes a line/side as input and positions the label at a configurable point along the edge with an outward offset.

---

## 8. Deriving Rotation Angles — General Method

Given a right triangle with legs a (along +x) and b (along +y) from the right-angle vertex:

1. **Identify** the target corner where the right angle should land
2. **Determine** which directions the legs must point from that corner (they must align with the frame edges)
3. **Find the rotation** that maps (+x, +y) to the required leg directions:
   - 0°: legs along (+x, +y)
   - 90°: legs along (+y, -x)
   - 180°: legs along (-x, -y)
   - -90°: legs along (-y, +x)
4. **Compute target** as the bounding-box center of the placed triangle

If the required leg directions don't match any of these four rotations, a **scale flip** (e.g., `[-1, 1, 1]`) is needed to change the triangle's chirality before rotating.

For this particular example with a ≠ b, all 8 placements are achievable with **pure rotations** (no reflections needed).
