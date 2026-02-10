# Quick Fix for Your Graph

## ❌ Your Current Graph (INVALID)

```
Circle ────────→ Transform (source input)
                        ↑
Square → Scale ────────┘ (target input)
```

**Problem:** Scale outputs an **Animation**, but Transform's target input expects a **Mobject (shape)**.

## Why This Crashes

1. `Square` creates a Mobject ✓
2. `Scale` takes that Mobject and returns an **Animation** (not a Mobject!)
3. `Transform` expects **two Mobjects** (source and target shapes to morph between)
4. You're feeding it an Animation instead of a Mobject → **Code generation fails**

---

## ✅ Correct Graph #1: Transform Between Two Shapes

If you want to morph a circle into a square:

```
Circle ──────source──→ Transform
Square ──────target──→ Transform
```

This creates the **square separately**, then morphs the **circle into the square**.

---

## ✅ Correct Graph #2: Scale a Square (No Transform)

If you want to scale a square:

```
Square → Scale
```

This creates a square and scales it up/down.

---

## ✅ Correct Graph #3: Multiple Independent Animations

```
Circle → Transform (need another shape for target!)
Square → Scale
Axes → Create
```

Each shape gets its own animation.

---

## What You Probably Want

Based on your graph, here are likely scenarios:

### Scenario A: Morph Circle → Square, then Scale the Result
**Problem:** You can't chain animations yet. The system doesn't support:
```
Circle → Transform → Scale  ❌ (not implemented)
```

**Workaround:** Just do the Transform:
```
Circle ──source──→ Transform
Square ──target──→ Transform
```

Then manually adjust the square's size properties **before** the transform.

### Scenario B: Just Scale a Square
```
Square → Scale
```

Set `scale_factor` to your desired size (e.g., 2.0 for 2x).

---

## Understanding Node Types

### Shape Nodes (Create Objects)
- **Output:** Mobject
- **Examples:** Circle, Square, Text, Axes
- **Connect to:** Animation nodes (FadeIn, Scale, Rotate, etc.)

### Animation Nodes (Animate Objects)
- **Input:** Mobject (the shape to animate)
- **Output:** Animation (the animation itself)
- **Examples:** FadeIn, Scale, Rotate, MoveTo
- **Connect to:** Nothing (they are terminal)

### Special Case: Transform
- **Inputs:**
  - `source` (Mobject) - Starting shape
  - `target` (Mobject) - Ending shape
- **Output:** Animation
- **Purpose:** Morph source into target

---

## Valid Connection Rules

✅ **Shape → Animation**
```
Circle → FadeIn
Square → Scale
Text → Write
```

✅ **Shape → Transform (both inputs)**
```
Circle ──source──→ Transform
Square ──target──→ Transform
```

❌ **Animation → Animation**
```
FadeIn → Scale  ❌ NOT SUPPORTED
```

❌ **Animation → Transform**
```
Scale → Transform  ❌ INVALID (what you tried)
```

---

## Try These Working Examples

### Example 1: Fade In a Circle
```
Circle → FadeIn
```

### Example 2: Scale a Square
```
Square → Scale (set scale_factor = 3.0)
```

### Example 3: Morph Circle to Square
```
Circle ──source──→ Transform
Square ──target──→ Transform
```

### Example 4: Multiple Shapes
```
Circle → FadeIn
Square → Scale
Text → Write
```

All three will animate independently.

---

## Next: Test a Simple Graph

1. **Delete all nodes** (start fresh)
2. **Add Circle** (from Shapes)
3. **Add Square** (from Shapes)
4. **Add Transform** (from Animations)
5. **Connect:**
   - Circle output (green dot) → Transform "source" input (blue dot)
   - Square output (green dot) → Transform "target" input (blue dot)
6. **Click "Render Preview"**

This should work! You'll see the circle morph into a square.

---

## Error Will Now Be Clearer

With the type checking I just added, your graph will now show:
```
Type mismatch: Scale outputs 'Animation' but Transform.target expects 'Mobject'
```

Much better than crashing!
