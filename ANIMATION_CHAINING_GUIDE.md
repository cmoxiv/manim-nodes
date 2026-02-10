# Animation Chaining & Visual Improvements

## ✅ What's New

### 1. Animation Nodes Now Output Both Animation AND Mobject

**Before:**
```
Circle → FadeIn → (animation only)
```

**Now:**
```
Circle → FadeIn → Rotate → Scale
         ↓        ↓        ↓
    (anim+mob) (anim+mob) (anim+mob)
```

Each animation node now has TWO outputs:
- **`animation`** (green) - The animation object (for Sequence)
- **`mobject_out`** (green) - The transformed mobject (for chaining)

---

### 2. Visual Distinction

**Node Colors:**
- 🔵 **Blue** - Shape nodes (Circle, Square, Text, etc.)
- 🟣 **Purple** - Animation nodes (FadeIn, Rotate, Scale, etc.)
- 🟢 **Green** - Math nodes (Axes, Vector, etc.)

**Handle Colors:**
- **Blue circles** - Regular inputs (left side)
- **Green circles** - Regular outputs (right side)
- **Orange squares** - Sequence chain handles (top/bottom)

**Sequence Node Layout:**
```
     [previous] ← Orange square at TOP
     ┌────────────┐
     │  Sequence  │
anim1→│            │
anim2→│            │
anim3→│            │
     └────────────┘
     [next] ← Orange square at BOTTOM
```

---

## How Animation Chaining Works

### The Concept

When you chain animations, each animation:
1. Takes a mobject as input
2. Creates an animation that will transform it
3. Outputs BOTH:
   - The animation (to add to Sequence)
   - The mobject reference (for next animation in chain)

**Key insight:** The original shape is NOT modified. Each animation in the chain operates on the same mobject, which gets transformed sequentially when the animations play.

---

## Example 1: Simple Chain

**Graph:**
```
Circle → FadeIn → Rotate → Scale
         │        │        │
         ↓ anim   ↓ anim   ↓ anim
         ↓        ↓        ↓
        Sequence.anim1    anim2     anim3
```

**Connections:**
1. Circle.output → FadeIn.mobject
2. FadeIn.mobject_out → Rotate.mobject
3. Rotate.mobject_out → Scale.mobject
4. FadeIn.animation → Sequence.anim1
5. Rotate.animation → Sequence.anim2
6. Scale.animation → Sequence.anim3

**Result:** Circle fades in → rotates → scales (in that order)

**Generated Code:**
```python
circle_1 = Circle()
self.add(circle_1)

fadein_1 = FadeIn(circle_1)
rotate_1 = Rotate(circle_1)  # Same mobject!
scale_1 = ScaleInPlace(circle_1)  # Same mobject!

self.play(fadein_1)
self.wait(0.5)
self.play(rotate_1)
self.wait(0.5)
self.play(scale_1)
```

---

## Example 2: Branching (Multiple Paths from One Shape)

**Graph:**
```
       Path 1: FadeIn → Rotate
       ↓        ↓
Circle ← Start  anim1   anim2 → Sequence1
       ↓
       Path 2: Scale → MoveTo
                ↓       ↓
               anim1   anim2 → Sequence2
```

**Two independent animation sequences using the SAME circle!**

---

## Example 3: Complex Multi-Object Scene

**Graph:**
```
Circle → FadeIn → Rotate → Scale → FadeOut
         ↓ anim   ↓ anim   ↓ anim   ↓ anim
         ↓        ↓        ↓        ↓
         ↓        ↓        ↓        ↓
Square → Create → MoveTo → Rotate
         ↓ anim   ↓ anim   ↓ anim
         ↓        ↓        ↓
Text   → Write
         ↓ anim
         ↓
        Sequence (all 8 animations)
```

**Result:** Complex orchestrated scene with multiple objects!

---

## Step-by-Step: Create Your First Chain

### 1. Add a Shape
- Add **Circle** from Shapes
- Notice it's **blue** colored

### 2. Add Animations in Chain
- Add **FadeIn** (purple node)
- Add **Rotate** (purple node)
- Add **Scale** (purple node)

### 3. Chain the Animations
Connect mobjects (shape flow):
1. Circle (green) → FadeIn.mobject (blue)
2. FadeIn.mobject_out (green) → Rotate.mobject (blue)
3. Rotate.mobject_out (green) → Scale.mobject (blue)

### 4. Add Sequence
- Add **Sequence** node
- Notice the **orange square** handles at top/bottom

### 5. Connect Animations to Sequence
Connect animation outputs (for timing):
1. FadeIn.animation (green) → Sequence.anim1 (blue)
2. Rotate.animation (green) → Sequence.anim2 (blue)
3. Scale.animation (green) → Sequence.anim3 (blue)

### 6. Render!
- Click "Render Preview"
- Watch your chained animation!

---

## Visual Guide: Understanding Handles

### Shape Nodes
```
┌─────────────┐
│   Circle    │ ← Blue background
│   (Shape)   │
└─────────────┘
              ● ← Green dot (mobject output)
```

### Animation Nodes
```
     ● ← Blue dot (mobject input)
┌─────────────┐
│   Rotate    │ ← Purple background
│ (Animation) │
└─────────────┘
         ● ← Green dot (animation output)
         ● ← Green dot (mobject_out output)
```

### Sequence Nodes
```
      ▪ ← Orange SQUARE (previous input)
┌─────────────┐
│  Sequence   │ ← Purple background
● anim1       │
● anim2       │
● anim3       │
└─────────────┘
      ▪ ← Orange SQUARE (next output)
```

---

## Rules & Best Practices

### ✅ Correct Patterns

**Linear chain:**
```
Shape → Anim1 → Anim2 → Anim3 → Anim4
```

**Branching from source:**
```
        → Anim1 → Anim2 → Sequence1
Shape →
        → Anim3 → Anim4 → Sequence2
```

**Multiple shapes, one sequence:**
```
Circle → FadeIn  → anim1
Square → Create  → anim2  → Sequence
Text   → Write   → anim3
```

### ❌ Common Mistakes

**Don't connect animation outputs to shape inputs:**
```
Circle → FadeIn.animation → Rotate  ❌ WRONG!
Use: FadeIn.mobject_out → Rotate.mobject
```

**Don't forget the dual connections:**
```
Circle → Rotate → Sequence  ❌ INCOMPLETE!

Correct:
Circle → Rotate.mobject
Rotate.mobject_out → (next animation if chaining)
Rotate.animation → Sequence.anim1
```

---

## FAQ

**Q: Why do animations have two outputs?**
A: To separate the animation (what to play) from the mobject (what to transform next). This allows chaining.

**Q: Does chaining modify the original shape?**
A: No! The original shape stays unchanged. You can use it for multiple animation branches.

**Q: What's the difference between mobject_out and animation outputs?**
- **mobject_out** → Connect to next animation's mobject input (for chaining)
- **animation** → Connect to Sequence's anim slots (for timing)

**Q: Why are sequence handles square and orange?**
A: To make them visually distinct from regular animation connections. They're for chaining Sequence nodes, not for connecting animations.

**Q: Can I connect mobject_out back to the same animation?**
A: No, that would create a circular dependency. Each animation in a chain must be different.

**Q: Do I need to use mobject_out if I'm not chaining?**
A: No! If you're just adding single animations to a Sequence, you only need to connect the animation outputs.

---

## Advanced: Combining Chains and Sequences

**Complex orchestration:**
```
Path 1: Shape1 → Anim1 → Anim2 → Anim3
                   ↓       ↓       ↓
                  seq1.1  seq1.2  seq1.3

Path 2: Shape2 → Anim4 → Anim5
                   ↓       ↓
                  seq2.1  seq2.2

Chained Sequences:
  Sequence1 (anim1, anim2, anim3) → Sequence2 (anim4, anim5)
```

This creates a complex timeline where paths execute in specific order!

---

## Troubleshooting

**"Type mismatch: Animation outputs 'Animation' but ... expects 'Mobject'"**
- You connected `.animation` to a mobject input
- Use `.mobject_out` instead for chaining

**"Orange squares not showing on Sequence node"**
- Refresh the frontend
- Make sure you're using the latest version
- The squares appear at TOP (previous) and BOTTOM (next)

**"Can't see different colors"**
- Make sure nodes were created after the update
- Delete and re-add nodes from the palette
- Colors: Blue=Shapes, Purple=Animations, Green=Math

**"Animation chain not working"**
- Check that mobject_out connects to next animation's mobject input
- Check that all animations connect their outputs to Sequence
- Verify no circular dependencies

---

## What This Enables

With animation chaining, you can now:
- ✅ Build complex multi-step transformations
- ✅ Reuse shapes for multiple animation paths
- ✅ Create intricate choreography with precise timing
- ✅ Combine with Sequence chaining for unlimited complexity

**You now have a professional-grade animation system! 🎬**
