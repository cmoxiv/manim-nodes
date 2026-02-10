# Manim Nodes - Usage Guide

## Understanding the Node System

### Node Types

#### 1. Shape Nodes (Green Output Dots)
Create visual objects (mobjects) in your scene:
- **Circle, Square, Rectangle** - Basic shapes
- **Line, Arrow** - Linear objects
- **Text** - Text labels
- **Axes, NumberPlane** - Coordinate systems
- **MathTex** - LaTeX mathematical expressions
- **Vector, Dot** - Mathematical objects

**Output:** Mobject (shape object)
**Connects to:** Animation nodes

#### 2. Animation Nodes (Blue Input + Green Output Dots)
Animate mobjects or create effects:
- **FadeIn, FadeOut** - Fade effects
- **Create, Write** - Drawing animations
- **Rotate, Scale, MoveTo** - Transform animations
- **Transform** - Morph one shape into another

**Input:** Mobject (the shape to animate)
**Output:** Animation
**Connects to:** Nothing (they are terminal nodes)

---

## How to Build Animations

### Basic Pattern

```
Shape Node → Animation Node
```

**Example:**
```
Circle → FadeIn
```

This creates a circle and fades it in.

---

## Answering Your Questions

### 1. Transform Node Requires Two Inputs

Transform morphs one shape into another. It needs:
- **Source** (blue dot labeled "source") - The starting shape
- **Target** (blue dot labeled "target") - The ending shape

**Example:**
```
Circle ---source--→ Transform
Square ---target--→ Transform
```

This morphs a circle into a square.

### 2. Move, Rotate, Scale Fixed! ✅

These nodes were using incorrect MANIM API calls. They're now fixed to use `.animate` syntax.

**Test them:**
- **MoveTo**: Circle → MoveTo (moves circle to a position)
- **Rotate**: Square → Rotate (rotates square 90°)
- **Scale**: Arrow → Scale (scales arrow by 2x)

### 3. What Can FadeIn Connect To?

**FadeIn outputs an Animation**, which is a terminal node.

**Correct:**
```
Circle → FadeIn
```

**Incorrect:**
```
Circle → FadeIn → FadeOut  ❌
```

Animations can't connect to other animations directly!

### 4. Multiple Animations (FadeIn + FadeOut)

To have both FadeIn and FadeOut on the same object:

**Current workaround:**
```
Circle → FadeIn
Circle → FadeOut
```

Connect the **same Circle** to **both animations**. They will execute in the order the nodes are processed (topological order).

**Known Issue:** Only the last animation plays because animations conflict. This is a limitation of the current architecture.

**Proper Solution (requires architecture change):**
We need to add a "Sequence" node to explicitly order animations.

### 5. Chaining Complex Effects

Your desired workflow:
```
1. Circle on 2D grid
2. Fade in
3. Rotate to 3D
4. Transform with matrix
5. Color/shade
6. Add text
7. Fade out
```

**Current Limitations:**
- ❌ 3D transformations (not implemented)
- ❌ Matrix transformations (no ApplyMatrix node)
- ❌ Sequential animation ordering
- ❌ Coloring animated objects

**What You CAN Do Now:**

```
[Circle] → [FadeIn]
[Square] → [FadeIn]
[Text] → [Write]
[Axes] → [Create]
```

**Recommended Approach for Complex Scenes:**

1. **Create all shapes first:**
   - Circle (with color properties set)
   - Text
   - Axes/NumberPlane

2. **Animate each shape separately:**
   - Circle → FadeIn
   - Text → Write
   - Axes → Create

3. **Transformations:**
   - Circle → Rotate (rotates the circle)
   - Circle → Scale (scales it)
   - Circle → MoveTo (moves it)

---

## Current Architecture Limitations

### ✅ What Works
- Creating shapes with properties (color, size, position)
- Animating individual shapes (fade, create, write)
- Transform between two shapes
- Basic transformations (rotate, scale, move)

### ❌ What Needs Implementation
- **Animation Sequencing** - Guaranteed order of animations
- **Animation Chaining** - FadeIn → Rotate → FadeOut on same object
- **3D Scenes** - ThreeDScene, 3D camera rotations
- **Matrix Transformations** - ApplyMatrix, custom transforms
- **Dynamic Coloring** - Changing colors during animation
- **Grouping** - VGroup for managing multiple objects
- **Advanced Animations** - Indicate, Flash, ShowPassingFlash

---

## Working Examples

### Example 1: Simple Fade In
```
Circle → FadeIn
```

### Example 2: Draw Multiple Shapes
```
Circle → Create
Square → Create
Arrow → Create
```

### Example 3: Transform Animation
```
Circle ──source──→ Transform
Square ──target──→ Transform
```

Circle morphs into a square.

### Example 4: Rotating Text
```
Text → Rotate
```

### Example 5: Math Visualization
```
Axes → Create
Circle → FadeIn
MathTex → Write
```

Creates coordinate axes, a circle, and mathematical text.

---

## Tips for Best Results

1. **Keep it simple** - Start with 1-2 shapes and 1-2 animations
2. **Test incrementally** - Add one node at a time and render
3. **Check connections** - Make sure green dots connect to blue dots
4. **Set properties** - Click nodes to edit colors, sizes, positions in the right panel
5. **Use Transform carefully** - It needs exactly 2 inputs (source and target)

---

## Future Roadmap

To support your use case (#5), we need to implement:

1. **Sequence Node** - Explicitly order animations:
   ```
   [Sequence]
   ├─ FadeIn (step 1)
   ├─ Rotate (step 2)
   └─ FadeOut (step 3)
   ```

2. **ApplyMatrix Node** - Matrix transformations

3. **ThreeDCamera Node** - 3D scene rotations

4. **SetColor/SetShading Nodes** - Dynamic styling

5. **VGroup Node** - Group multiple objects

Would you like me to implement any of these features?

---

## Getting Help

- Check backend logs for detailed error messages
- Frontend shows "Render Error" when generation fails
- Look at the generated Python code (we can add a code viewer)

## Testing Your Fixes

Try these now that Move/Rotate/Scale are fixed:

1. **Rotating Circle:**
   ```
   Circle → Rotate (set angle to 180°)
   ```

2. **Scaling Square:**
   ```
   Square → Scale (set scale_factor to 3.0)
   ```

3. **Moving Arrow:**
   ```
   Arrow → MoveTo (set target to x=2, y=3)
   ```

Let me know what works and what doesn't!
