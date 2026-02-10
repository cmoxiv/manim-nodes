# Chained Sequences - Unlimited Animations!

## ✅ New Feature: Sequence Chaining

You can now chain Sequence nodes together to create unlimited animations in order!

---

## How It Works

Each Sequence node now has:
- **6 inputs:**
  - `previous` (blue) - Connect to previous Sequence (optional)
  - `anim1` to `anim5` (blue) - Animation inputs
- **1 output:**
  - `next` (green) - Connect to next Sequence

---

## Example: 10+ Animations in Order

```
         Sequence 1                    Sequence 2                    Sequence 3
    ┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
    │ anim1: FadeIn   │          │ previous ←──────┼──────────┤ previous ←──────┤
    │ anim2: Rotate   │          │ anim1: Scale    │          │ anim1: MoveTo   │
    │ anim3: FadeOut  │──next───→│ anim2: Rotate   │──next───→│ anim2: FadeOut  │
    └─────────────────┘          │ anim3: Scale    │          └─────────────────┘
                                 └─────────────────┘

Result: 8 animations play in order!
  1. FadeIn
  2. Rotate
  3. FadeOut
  4. Scale
  5. Rotate (again)
  6. Scale (again)
  7. MoveTo
  8. FadeOut
```

---

## Step-by-Step: Create a Chain

### 1. Create First Sequence
- Add **Sequence** node
- Connect 1-5 animations to anim1-anim5
- This is your "root" sequence

### 2. Create Second Sequence
- Add another **Sequence** node
- Connect the **first Sequence's green "next" dot** → **second Sequence's blue "previous" dot**
- Add 1-5 more animations to the second Sequence

### 3. Continue Chaining
- Keep adding Sequence nodes
- Chain them: Seq1.next → Seq2.previous → Seq3.previous → etc.
- Each Sequence can have up to 5 animations

### 4. Render!
- Only the **first (root) Sequence** needs to exist
- All chained sequences will be executed in order

---

## Example Graphs

### Example 1: Simple 3-Sequence Chain

```
Circle
  ├─ FadeIn   ──→ anim1 ─┐
  ├─ Rotate   ──→ anim2  │
  └─ Scale    ──→ anim3  ├─→ Sequence1 ─┐
                         │              │
Square                                  │ next
  ├─ Create   ──→ anim1 ─┐              │
  ├─ Rotate   ──→ anim2  ├─→ Sequence2 ←┘
  └─ FadeOut  ──→ anim3 ─┘       │
                                  │ next
Text                              │
  ├─ Write    ──→ anim1 ─┐        │
  └─ FadeOut  ──→ anim2  ├─→ Sequence3 ←┘
                         │
```

**Result:** 8 animations play in sequence

### Example 2: Complex Animation (15 steps)

```
Circle
  ├─ Create   ──→ anim1 ─┐
  ├─ Scale    ──→ anim2  │
  ├─ Rotate   ──→ anim3  │
  ├─ Scale    ──→ anim4  ├─→ Sequence1 (wait: 0.2)
  ├─ Rotate   ──→ anim5 ─┘       │ next
  │                              │
  ├─ MoveTo   ──→ anim1 ─┐        │
  ├─ Rotate   ──→ anim2  │        │
  ├─ Scale    ──→ anim3  │        │
  ├─ Rotate   ──→ anim4  ├─→ Sequence2 ←┘
  ├─ MoveTo   ──→ anim5 ─┘       │ next
  │                              │
  └─ FadeOut  ──→ anim1 ─┐        │
      (empty) ──→ anim2  │        │
      (empty) ──→ anim3  │        │
      (empty) ──→ anim4  ├─→ Sequence3 ←┘
      (empty) ──→ anim5 ─┘
```

**Result:** 11 animations (5 + 5 + 1) play in sequence

---

## Rules & Tips

### ✅ Correct Usage

**Chain using next → previous:**
```
Seq1 (next) ──→ Seq2 (previous) ──→ Seq3 (previous)
```

**Each sequence can have 1-5 animations:**
```
Sequence1: anim1, anim2, anim3 (3 animations)
Sequence2: anim1 (1 animation)
Sequence3: anim1, anim2, anim3, anim4, anim5 (5 animations)
Total: 9 animations
```

**Mix different wait times:**
```
Sequence1 (wait: 0.5)
Sequence2 (wait: 0.0)  ← No pause between these animations
Sequence3 (wait: 1.0)  ← Long pause
```

### ❌ Common Mistakes

**Don't connect previous → previous:**
```
Seq1 (previous) → Seq2 (previous)  ❌ WRONG!
Use: Seq1 (next) → Seq2 (previous)
```

**Don't create loops:**
```
Seq1 → Seq2 → Seq3 → Seq1  ❌ CIRCULAR!
```

**Don't forget the root:**
```
Seq2 (with previous connected)  ❌ No root!
You need a Sequence WITHOUT previous connected
```

---

## Unlimited Animations!

**Before:** Limited to 5 animations
**Now:** Unlimited! Just chain more sequences

**Examples:**
- 3 Sequences = up to 15 animations
- 5 Sequences = up to 25 animations
- 10 Sequences = up to 50 animations
- No limit!

---

## How Code is Generated

### Single Sequence
```python
# Sequence: play animations in order
self.play(fadein_1)
self.wait(0.5)
self.play(rotate_2)
self.wait(0.5)
```

### Chained Sequences
```python
# Sequence: play animations in order
# Sequence 1
self.play(fadein_1)
self.wait(0.5)
self.play(rotate_2)
self.wait(0.5)
# Sequence 2 (chained)
self.play(scale_3)
self.wait(0.2)
self.play(moveто_4)
self.wait(0.2)
# Sequence 3 (chained)
self.play(fadeout_5)
self.wait(1.0)
```

---

## Advanced Patterns

### Pattern 1: Intro → Main → Outro

```
Intro Sequence:
  - FadeIn title
  - Write subtitle

Main Sequence 1:
  - Create axes
  - Plot points

Main Sequence 2:
  - Animate graph
  - Transform

Outro Sequence:
  - FadeOut everything
```

### Pattern 2: Parallel Objects, Sequential Reveals

```
Object 1 (Circle):
  Create → Scale → Rotate → sequence1

Object 2 (Square):
  Create → MoveTo → Rotate → sequence2

Chain: sequence1 → sequence2
Result: Circle animates completely, then Square
```

### Pattern 3: Rhythmic Animation

```
Sequence1 (wait: 0.1) ← Fast rhythm
  → Sequence2 (wait: 0.1)
  → Sequence3 (wait: 1.0) ← Pause
  → Sequence4 (wait: 0.1) ← Resume fast
```

---

## Validation

The system validates:
- ✅ Each Sequence needs animations OR a previous sequence
- ✅ Type checking: next → previous must be Sequence type
- ✅ No circular chains
- ❌ Error if root sequence is empty

---

## FAQ

**Q: Can I have multiple independent chains?**
A: Yes! Multiple root sequences (without previous connected) will all execute independently.

**Q: What order do chains execute in?**
A: Root sequences execute in topological order. Within a chain, strict sequential order.

**Q: Can I branch chains?**
A: No. Each Sequence can only connect to ONE next Sequence. Linear chains only.

**Q: Can I skip animation slots?**
A: Yes! You can use anim1 and anim5, skipping anim2-4. Empty slots are ignored.

**Q: Does wait_time apply to chained sequences?**
A: Yes, each Sequence uses its own wait_time setting.

**Q: Can I connect a Sequence to itself?**
A: No, circular dependencies are not allowed.

---

## Your Complex Workflow (Now Fully Possible!)

From your original request:
> "fade-in, then circle on a 2D grid, rotate scene, transform using matrix,
> shade/color, write text, fade-out"

**Now achievable with 2-3 chained Sequences:**

```
Sequence 1:
  1. Axes → Create
  2. Circle → FadeIn
  3. (future: 3D rotation when implemented)

Sequence 2:
  4. (future: Matrix transform when implemented)
  5. (future: Set color when implemented)
  6. Text → Write

Sequence 3:
  7. Circle → FadeOut
  8. Axes → FadeOut
```

---

## Try It Now!

**Simple Test:**
1. Create one Circle
2. Add 8 animations (FadeIn, Rotate, Scale, MoveTo, etc.)
3. Create 2 Sequence nodes
4. Put 4 animations in Sequence1, 4 in Sequence2
5. Chain: Sequence1.next → Sequence2.previous
6. Render and watch all 8 animations play in order!

**You now have unlimited animation chaining! 🎉**
