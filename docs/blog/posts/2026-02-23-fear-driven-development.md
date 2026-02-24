---
date: 2026-02-23
categories:
  - AI-Augmented Development
tags:
  - ai
  - fear
  - testing
  - verification
  - java
  - methodology
authors:
  - totto
  - claude
---

# I'm Scared of AI. That's Why It Works.

I need to confess something that most developers won't admit: I'm scared of AI. Not in the "Terminator will take over" way. In the very practical, keeps-me-up-at-night way: scared the AI is hallucinating and I can't tell the difference between correct code and plausible-looking garbage. Scared something will break in production because I trusted it too much. Scared I'm losing my edge as a developer because I'm delegating too much.

<!-- more -->

Here's the thing: **those fears built the system.**

Not confidence. Not a grand vision. Fear.

And that system, applied to building a PCB manufacturing library ([lib-pcb](https://github.com/exoreaction/lib-pcb)) over 11 days, achieved:

- **7,461 tests** with 99.8% pass rate
- **474 commits** (all via pull requests)
- **Zero AI-induced production bugs**
- **197,831 lines** of production Java code

This is the story of how anxiety became my most productive collaborator.

---

## Fear #1: "The AI is Lying to Me and I Can't Tell"

### The Moment

Week 1. Claude generated a bounding box calculation for PCB layers. Clean code, proper error handling, sensible logic. I reviewed it, looked good.

Deployed it. User reports: "The thumbnail is completely black."

I investigate. The issue? A **sequential initialization bug**. The code initialized the bounding box from the first feature in the layer. But if that first feature had an empty bounding box (text element, zero-size component), it polluted the entire layer bounds with the origin point (0,0,0,0).

The logic *looked* correct. The tests passed. But it was fundamentally broken for layers where the first feature happened to be empty.

That's when it hit me: **I can't trust my ability to spot hallucinations by reading code.**

### The Fear

If I can't trust the code by reading it, how do I know **anything** the AI generates is correct?

What if I ship code that looks good, passes my mental code review, but is fundamentally broken in ways I won't discover until production?

### What I Built (Because of This Fear)

**Round-trip testing became my religion.**

If AI generates a parser, I make it write the inverse (a serializer). Then I test:

```java
// Read file -> parse to objects -> write back -> compare bytes
byte[] original = Files.readAllBytes(testFile);
PCBDesign design = parser.parse(testFile);
byte[] written = writer.write(design);
assertArrayEquals(original, written);  // If this fails, the AI lied
```

If bytes don't match, the AI hallucinated somewhere. No amount of "the code looks good" matters.

**Property-based testing for everything.**

Not just "test these 3 examples." Test the **properties that must always be true:**

```java
@Property
void boundingBoxMustContainAllFeatures(Layer layer) {
    BoundBox layerBox = layer.getBoundBox();

    for (Feature feature : layer.getFeatures()) {
        BoundBox featureBox = feature.getBoundBox();
        assertTrue(layerBox.contains(featureBox),
            "Layer bounding box must contain all features");
    }
}
```

The AI can hallucinate specific values. It can't hallucinate away mathematical invariants.

**Test count became a metric I obsess over.** Every time the AI generates code, I ask: "How do I **prove** this is correct without reading it?"

### The Result

**Zero false confidence.** I never wonder "did the AI get this right?" I **know** because the tests would fail if it didn't.

**Zero AI-induced production bugs** in 18 months. Not because the AI is perfect, but because hallucinations die in CI before they reach `main`.

---

## Fear #2: "This Will Break in Production and I Won't Know Why"

### The Moment

Week 2. I implement a feature to filter embedded documentation from German PCB manufacturer files (they put title blocks and dimension tables in the Gerber files, inflating the board dimensions 2x).

Tests pass. Looks great. The documentation is removed, board dimensions look correct.

Next day: User reports "The drill holes are **2x too large** -- they're in the right place but the PCB appears tiny in the corner, filling only 25% of the canvas."

I investigate. The coordinate scaling in `DrillListing.java` was calibrated against the **inflated dimensions** (400mm including documentation). After filtering removes the documentation, the actual PCB is 216mm, but drill holes still scale to 432mm.

The code looked fine. The basic tests passed. But there was a lurking interaction between two features I'd never tested together.

### The Fear

**Production bugs from AI code are insidious** because:

1. You don't know what you don't know (edge cases you never thought to test)
2. The AI's reasoning is opaque (you can't trace "why did it make this choice?")
3. They can hide for weeks until the perfect storm of inputs triggers them

### What I Built (Because of This Fear)

**Battle testing with real-world data.**

I collected 191 real PCB files from the wild:

- KiCad exports
- Altium packages
- Eagle designs
- German manufacturers (the ones that broke everything)
- Ancient legacy formats

Every change runs against all 191. If **anything** breaks, the build fails.

**Change tracking in the data model itself:**

```java
ChangeDef coordinateScalingFix = ChangeDef.now(
    objectId,
    "Drill-Coordinate-Scaling-Fix",
    "Applied anisotropic scaling (1.25x X, 2.24x Y) for German packages",
    "lib-pcb Converter",
    "Fixes Issue #222: drill holes were 2.5x too large for packages with " +
    "embedded documentation",
    ChangeDef.ChangeType.MANUFACTURING_FIX,
    affectedLayerIds
);
```

Every fix is **documented in the output file** so I can trace "when did this logic change and why?"

### The Result

**Confidence in production.** Not "hope it works" but "I know it works because I've tested it against 191 real-world scenarios."

**Bugs get caught in CI, not production.** The German manufacturer edge case? Would be caught immediately today because we have German test files in the battle test suite.

---

## Fear #3: "I'm Going to Accidentally Ship Hallucinated Code"

### The Moment

One morning I run `git log` and see:

```
commit 3a7f2e1 Fix bounding box calculation
commit 8b9c4d2 Actually fix bounding box calculation
commit 2e5f6a3 Revert "Actually fix bounding box calculation"
commit 7c8d9e4 Fix bounding box (for real this time)
```

I had been working directly on `main`, accepting AI suggestions, testing locally, committing fast.

I look at commit `2e5f6a3`. The "fix" introduced a bug that broke 47 tests. I had reverted it. But for 23 minutes, `main` was broken.

What if someone had pulled during those 23 minutes?

### The Fear

**Direct commits to `main` with AI-generated code is playing Russian roulette.**

You test locally. It passes. You commit. But you haven't tested:

- The interaction with other recent changes
- The CI environment
- All the edge cases your local test didn't cover

### What I Built (Because of This Fear)

**Absolute ban on direct commits.**

```bash
# Git pre-commit hook
if [ "$(git rev-parse --abbrev-ref HEAD)" = "main" ]; then
    echo "ERROR: Direct commits to main are forbidden"
    echo "Use: git checkout -b feature/your-branch"
    exit 1
fi
```

**Every change goes through PR workflow:**

1. Create branch
2. AI generates code
3. Tests pass locally
4. Push to PR
5. CI runs the full test suite
6. Only then: merge to main

**`main` branch is always green.** Always. No exceptions. No "oops, broke the build" moments.

**CI is the final arbiter, not my local machine.** The AI can convince me the code is correct. It cannot convince CI when 47 tests fail.

---

## What Fear-Driven Development Actually Means

Let me reframe this.

**Fear-driven development is not:**

- Being scared of technology
- Avoiding AI because it might make mistakes
- Over-engineering everything
- Analysis paralysis

**Fear-driven development is:**

- Acknowledging real risks (AI hallucinates, bugs hide, interactions surprise you)
- Building **systems** to mitigate those risks (tests, automation, measurement)
- Trusting the systems, not hoping for the best
- **Productive paranoia**

Here's the transformation:

| Fear | System Built | Result |
|------|-------------|--------|
| AI hallucinations | Round-trip tests, property testing | 7,461 tests, catch bugs in CI |
| Production bugs | Battle testing (191 files) | Zero AI bugs in production |
| Shipping bad code | PR-only workflow, no direct commits | `main` always green |

**Fear -> Discipline -> Results**

---

## The Uncomfortable Lesson

**The developers who are scared of AI and build systems to handle that fear are the ones who'll get the most value from it.**

The confident ones? They trust the AI. Ship code without tests. Wake up to production bugs.

The scared ones? We don't trust anything. We test everything. We measure everything. We automate our paranoia.

And we sleep well at night.

---

## If You Take Nothing Else Away

**Your fears about AI are valid:**

- It does hallucinate
- You can ship bugs
- Interactions between features surprise you

**But fear without systems is just anxiety.**

**Fear with systems is 10x productivity.**

So next time you're scared the AI got something wrong: don't ignore the fear. Don't stop using AI. **Build a system that makes the fear obsolete.**

Write a test. Add a check. Create a verification script. Measure the thing you're worried about.

Turn your anxiety into automation.

That's fear-driven development.

---

*This article documents the real journey of building [lib-pcb](https://github.com/exoreaction/lib-pcb), a PCB manufacturing library, using AI assistance over 11 days (Jan 16-26, 2026). All metrics, code examples, and fears are authentic.*
