---
date: 2026-02-17
categories:
  - AI-Augmented Development
tags:
  - ai
  - fear
  - testing
  - verification
  - java
  - methodology
  - cost
  - control
authors:
  - totto
---

# The Hallucination Tax: Three More Fears That Made My AI Workflow Better

The [last post](2026-02-27-fear-driven-development.md) was about hallucinations, production bugs, and shipping bad code. Three fears that built three systems. This post is about the next three: money, control, and silence.

<!-- more -->

Same project. Same 11 days building [lib-pcb](https://github.com/exoreaction/lib-pcb). Same pattern: a fear shows up, I can't ignore it, so I build something to deal with it.

These three are different from the first batch. The first three were technical. These are existential. What happens when the economics don't work? What happens when you stop understanding your own code? What happens when everything looks fine but isn't?

---

## Fear #4: "The Costs Will Spiral Out of Control"

### The Moment

Week 1. I'm deep in lib-pcb, running multiple Claude sessions per day, long context windows, heavy code generation. Parser development, test creation, architecture decisions.

I do the math on standard API pricing.

Estimated cost for this project at pay-per-token rates: **$100,000.**

Not per year. For one 2.5-week project.

### The Fear

At standard API pricing, fear-driven development is economically impossible. Testing everything, verifying everything, measuring everything. All of that requires tokens. Massive amounts of tokens.

And I've built my entire workflow around using AI liberally. Not as an occasional assistant, but as a constant collaborator. What if the pricing model changes? What if unlimited access goes away?

### What I Built (Because of This Fear)

**Claude MAX subscription became non-negotiable infrastructure.** Like electricity. Without unlimited usage, my approach doesn't work. The economics are binary: with a flat subscription, fear-driven development is the obvious strategy (test more, verify more, explore more). With pay-per-token, you start rationing. Rationing AI usage means rationing verification. Which means rationing quality.

Even with unlimited access, **strategic model selection matters.** Not for cost, but for clarity and speed:

- **Haiku** for simple, well-defined tasks (formatting, boilerplate, straightforward queries)
- **Sonnet** for most coding (implementation, test writing, refactoring)
- **Opus** for architecture decisions, complex analysis, and novel problem-solving

The discipline isn't about saving money. It's about matching the tool to the task.

And underneath: **a quiet awareness that this could change.** The methodology works regardless of which AI you use. The subscription makes it practical. But if I had to switch tomorrow, the systems would survive.

### The Result

**The hallucination tax is real, and it's worth paying.** Every verification step, every round-trip test, every "let me check this against real data" costs tokens. On a per-token basis, that's expensive. On a flat subscription, it's free. And the alternative (shipping unverified code) is far more expensive in production bugs, reputation, and sleep.

---

## Fear #5: "I'm Losing Control to the AI"

### The Moment

Working on a complex refactoring of the coordinate system. I give Claude a high-level description of what needs to change. Claude produces a plan. I read it, nod, say "looks good, do it."

An hour later: **47 changed files.** I start reviewing. I understand the overall direction. I understand maybe 60% of the specific changes. Tests pass. Everything works.

But I sit there looking at the diff and think: "I just shipped code I don't fully understand."

And then the harder thought: "Am I still a developer if the AI is doing the thinking?"

### The Fear

The more capable AI becomes, the more you can delegate. The more you delegate, the less you understand your own codebase. There's a comfort gradient that slopes toward ignorance.

I've been writing software for 30 years. I've built enterprise architectures, led development teams, designed systems that are still running. The idea that I'm becoming a spectator in my own codebase is not a theoretical concern. It's an identity concern.

### What I Built (Because of This Fear)

**Directed synthesis.** The name matters. "Directed" means I'm driving. "Synthesis" means the AI is combining information, not making decisions.

The workflow, every time:

1. **I** identify the problem and decide the approach
2. **AI** explores the codebase, finds relevant files, maps dependencies
3. **I** review the findings and decide what to change
4. **AI** implements changes to my specification
5. **I** review every change, understand every file
6. **AI** runs tests and reports results
7. **I** make the merge decision

Seven steps. Four are mine. Three are the AI's. And the AI's three are all execution, not judgment.

More importantly: **explicit task breakdown replaced vague delegation.** After the 47-file incident, I stopped saying "refactor the coordinate system." Instead:

- "Show me every file that references `BoundBox.getWidth()`"
- "In `GerberParser.java`, change the scaling from absolute to relative"
- "Write a test that verifies drill coordinates survive a round-trip through the new system"

Each task is small enough that I understand it completely. The AI does the typing. I do the thinking.

Is it slower than "just do the whole thing"? Yes. Is it worth it? I can explain every line in the codebase. I know why every architectural decision was made. So yes.

### The Result

**Better understanding, not less.** This is the counterintuitive outcome. Before AI, I understood my code because I wrote it. With AI and vague delegation, I understood less because I didn't. With AI and directed synthesis, I understand *more* because I'm forced to articulate what I want before the AI builds it. The articulation is the understanding.

I'm not a spectator. I'm a director. The distinction matters to me.

---

## Fear #6: "Silent Failures. Something Broke and Nobody Noticed."

### The Moment

A user reports: "The PCB bounding box is wrong. The board should be 216mm wide, but your library says 425mm."

I check. Individual drill holes: right place. Tested. Assembly components: right place. Tested. Layer alignment: correct. Tested.

Everything that's tested is correct.

But the overall bounding box calculation was including a documentation layer with inflated coordinates. A German manufacturer had embedded title blocks and dimension tables in the Gerber output, and those elements extended far beyond the actual board edge.

Tests were green. The code worked. But the *result* was wrong because the wrong thing was being measured.

### The Fear

**Green tests don't mean the system is correct. They mean the system matches what you tested.**

This is the quietest fear, and the most dangerous one. The first five fears announce themselves. This one doesn't. Silent failures look exactly like success until someone compares the output to reality.

With AI-generated code, the surface area for silent failures is enormous. The AI can write perfect logic for the wrong problem. It can implement a flawless calculation on incorrect assumptions. And you'll never know until a human with domain knowledge looks at the output and says "that number is wrong."

### What I Built (Because of This Fear)

**Extreme measurement culture.** Every significant value gets logged and verified against expectations:

```java
System.out.printf("PCB boundBox: %.1fmm × %.1fmm\n",
    width / 1_000_000.0, height / 1_000_000.0);
System.out.printf("Expected: ~216mm × 206mm\n");
assertTrue(misalignment < 0.25,
    "BoundBox should be within 25% of copper layer dimensions");
```

Not just "did it crash?" but "are the values reasonable?"

**Sanity checks at every boundary.** If a PCB dimension exceeds 1 meter, something is wrong. If a drill hole has a negative diameter, something is wrong. If a layer has zero features after parsing a 500KB file, something is wrong. These are not functional tests. They're reality checks.

**Metrics tracking over time.** Test count should increase. Pass rate should stay above 99%. Battle test pass rate should be 100%. If any trend line moves the wrong direction, I want to know before a user does.

The principle: **measure the thing, not just the process that produces the thing.** Tests verify logic. Measurements verify reality.

### The Result

**Bugs surface in development, not production.** The bounding box issue would be caught immediately today because every parsed file reports its dimensions, and any dimension that deviates more than 25% from the copper layer bounds triggers a warning.

The silence is gone. Everything speaks.

---

## The Pattern, Again

| Fear | System Built | Result |
|------|-------------|--------|
| Cost spiral | Claude MAX + strategic model selection | $100K API costs become unlimited |
| Losing control | Directed synthesis, explicit task breakdown | Better understanding, not less |
| Silent failures | Extreme measurement, sanity checks | Bugs surface in dev, not production |

**Fear #4** is about economics. Build a workflow that assumes abundant AI access, because rationing verification is rationing quality.

**Fear #5** is about identity. Stay in the driver's seat. The AI is fast but you're the one who knows where to go.

**Fear #6** is about epistemology. Passing tests prove your logic is consistent. Measurement proves your output is correct. They're not the same thing.

---

## What I Don't Know

I don't know if this generalizes beyond my situation. I have 30 years of context that informs which tasks to delegate and which to keep. A junior developer using directed synthesis might direct the AI to the wrong place. An experienced developer who skips measurement might catch silent failures through intuition.

What I do know: these fears were useful. Every one of them pointed at something real. And every system I built because of them is still running, still catching problems, still keeping `main` green.

There are more fears. The next post will cover the last three.

---

*This is Part 2 of the Fear-Driven Development series. [Part 1](2026-02-27-fear-driven-development.md) covered hallucinations, production bugs, and direct commits. Part 3 will cover the final three fears. All examples are from building [lib-pcb](https://github.com/exoreaction/lib-pcb) over 11 days (Jan 16-26, 2026).*
