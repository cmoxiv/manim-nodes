# Sequence Node - Animation Chaining

## ✅ Now Implemented!

The **Sequence** node lets you chain animations in a specific order.

---

## How It Works

The Sequence node has **5 animation inputs** (anim1, anim2, anim3, anim4, anim5):
- Connect animations to these inputs
- They'll play **in order**: anim1 → anim2 → anim3 → etc.
- You don't need to use all 5 (minimum: 1 animation)
- Each animation has an optional **wait_time** pause after it

---

## Example 1: Fade In → Rotate → Fade Out

```
         ┌─────────┐
         │ Circle  │
         └────┬────┘
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
    ▼         ▼         ▼         │
┌────────┐ ┌────────┐ ┌────────┐ │
│ FadeIn │ │ Rotate │ │ FadeOut│ │
└───┬────┘ └───┬────┘ └───┬────┘ │
    │          │          │       │
    │ anim1    │ anim2    │ anim3 │
    └──────────┴──────────┴───────┘
              │
        ┌──────────┐
        │ Sequence │
        └──────────┘
```

**Result:** Circle fades in → rotates → fades out

---

## Example 2: Multiple Shapes, Sequential Animations

```
┌────────┐    ┌────────┐
│ Circle │    │ Square │
└───┬────┘    └───┬────┘
    │             │
    ▼             ▼
┌────────┐    ┌────────┐
│ Create │    │ FadeIn │
└───┬────┘    └───┬────┘
    │ anim1       │ anim2
    └─────────────┘
          │
    ┌──────────┐
    │ Sequence │
    └──────────┘
```

**Result:** Circle appears (Create) → then Square fades in

---

## Example 3: Complex Chain (5 animations)

```
Circle
  ├─ FadeIn   ──→ anim1
  ├─ Rotate   ──→ anim2
  ├─ Scale    ──→ anim3
  ├─ MoveTo   ──→ anim4
  └─ FadeOut  ──→ anim5
            │
      ┌──────────┐
      │ Sequence │
      │ wait: 0.3│
      └──────────┘
```

**Result:**
1. Circle fades in
2. *wait 0.3s*
3. Circle rotates
4. *wait 0.3s*
5. Circle scales up
6. *wait 0.3s*
7. Circle moves to new position
8. *wait 0.3s*
9. Circle fades out

---

## Step-by-Step: Create Your First Sequence

### 1. Create a Shape
- Add **Circle** from Shapes category

### 2. Create Animations
- Add **FadeIn** from Animations
- Add **Rotate** from Animations
- Add **FadeOut** from Animations

### 3. Connect Shape to Animations
- Connect Circle (green dot) → FadeIn (blue "mobject" input)
- Connect Circle (green dot) → Rotate (blue "mobject" input)
- Connect Circle (green dot) → FadeOut (blue "mobject" input)

### 4. Add Sequence Node
- Add **Sequence** from Animations category
- You'll see 5 blue input dots labeled: anim1, anim2, anim3, anim4, anim5

### 5. Connect Animations to Sequence (in order!)
- Connect FadeIn (green dot) → Sequence anim1 (blue dot)
- Connect Rotate (green dot) → Sequence anim2 (blue dot)
- Connect FadeOut (green dot) → Sequence anim3 (blue dot)

### 6. Configure Wait Time (optional)
- Click the **Sequence** node
- In the right panel, adjust **wait_time** (default: 0.5 seconds)
- This is the pause **between** each animation

### 7. Render!
- Click **"Render Preview"**
- Watch your animation chain!

---

## Properties

### Sequence Node Properties
- **wait_time** (0.0 - 5.0 seconds)
  - Pause duration **after** each animation
  - Default: 0.5 seconds
  - Set to 0 for no pause (animations play immediately back-to-back)

---

## Important Notes

### ✅ Correct Usage

**Multiple animations on the SAME object:**
```
Circle → FadeIn  ──→ anim1 ─┐
      → Rotate  ──→ anim2  ├─→ Sequence
      → FadeOut ──→ anim3 ─┘
```

**Multiple objects, sequential reveals:**
```
Circle → Create ──→ anim1 ─┐
Square → FadeIn ──→ anim2  ├─→ Sequence
Text   → Write  ──→ anim3 ─┘
```

### ❌ Common Mistakes

**Don't connect shapes to Sequence:**
```
Circle ──→ Sequence  ❌ WRONG!
```
Sequence expects **Animation** inputs, not shapes!

**Don't skip anim1:**
```
FadeIn → anim3  ❌ Use anim1, anim2, anim3 in order
```
Always start with anim1, then anim2, etc.

---

## Advanced Usage

### Nested Sequences?
Not currently supported. You can't connect a Sequence to another Sequence.

**Workaround:** Use all 5 animation slots in one Sequence node.

### More than 5 animations?
Not supported yet. Current limit is 5 animations per Sequence.

**Workaround:** Create multiple Sequence nodes and time them carefully.

---

## Examples to Try

### Example A: Pulsing Circle
```
Circle
  ├─ Create ──→ anim1 ─┐
  ├─ Scale(3x) → anim2 │
  └─ Scale(1x) → anim3 ├─→ Sequence (wait: 0.2)
                       │
```
Creates a circle that pulses (grows then shrinks).

### Example B: Moving and Spinning Square
```
Square
  ├─ FadeIn  ──→ anim1 ─┐
  ├─ Rotate  ──→ anim2  │
  ├─ MoveTo  ──→ anim3  ├─→ Sequence (wait: 0.5)
  └─ FadeOut ──→ anim4 ─┘
```

### Example C: Math Animation
```
Axes → Create  ──→ anim1 ─┐
Circle → FadeIn ──→ anim2 │
Text → Write  ──→ anim3  ├─→ Sequence (wait: 1.0)
                        │
```
Sets up a coordinate system, adds a circle, then labels it.

---

## Troubleshooting

**"Sequence node needs at least one animation connected"**
- You created a Sequence but didn't connect any animations
- Connect at least one animation to anim1

**"Type mismatch: ... outputs 'Mobject' but Sequence.anim1 expects 'Animation'"**
- You connected a shape directly to Sequence
- Shapes must go through an animation node first:
  - Circle → FadeIn → Sequence ✅
  - Circle → Sequence ❌

**Animations playing in wrong order**
- Check which anim slot you connected to
- They play in order: anim1, anim2, anim3, anim4, anim5
- You can skip slots (e.g., use only anim1 and anim3)

**Some animations not playing**
- Make sure they're connected to the Sequence
- Check that the green dots (animation outputs) connect to blue dots (Sequence inputs)

---

## What This Enables

Now you can create:
- ✅ **Multi-step reveals** (appear, rotate, disappear)
- ✅ **Transformations** (morph, scale, move)
- ✅ **Storytelling** (show axes, plot point, label, explain)
- ✅ **Your complex workflow from Question #5!**

---

## Your Complex Workflow (Now Possible!)

From your original request:
> "fade-in, then circle on a 2D grid, rotate scene to convert to 3D grid/axes,
> then transform the circle using a matrix, shade or colour the transformed sphere,
> write some text, and then fade-out"

**What you can do NOW:**
```
Axes → Create    ──→ anim1 ─┐
Circle → FadeIn  ──→ anim2  │
Circle → Rotate  ──→ anim3  │
Text → Write    ──→ anim4  ├─→ Sequence
Circle → FadeOut ──→ anim5 ─┘
```

**What's still missing:**
- 3D scene rotation (requires ThreeDCamera node - not implemented)
- Matrix transformations (requires ApplyMatrix node - not implemented)
- Dynamic coloring (requires SetColor node - not implemented)

But you can now **chain effects in sequence**, which is the core capability you needed!

---

## Next Steps

1. **Test the Sequence node** with a simple 3-animation chain
2. **Try the examples** above
3. **Report any bugs** you find

Would you like me to add:
- More animation slots (10 instead of 5)?
- Parallel animation support (play multiple at once)?
- Loop/repeat functionality?
- 3D nodes for your full workflow?

Let me know what works and what doesn't!
