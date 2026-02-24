---
date: 2026-01-22
categories:
  - AI-Augmented Development
tags:
  - ai
  - architecture
  - methodology
  - career
  - delegation
  - workflow
authors:
  - totto
  - claude
---

# Strategic Delegation: When Developers Become Architects

For thirty years I have broken work into tasks. Decompose the feature into subtasks, estimate the hours, write the code, move the ticket. The unit of progress was the line of code. The measure of a good day was how much I shipped. That loop was so deeply embedded in how I worked that I did not notice it was a loop. It was just what development meant.

Then I started delegating implementation to AI, and the loop broke. Not gradually. In about a week.

<!-- more -->

The shift was not from writing code to not writing code. It was from thinking about *how* to implement something to thinking about *what* to implement and *why*. The how became cheap. The what and why did not. And that inversion, once you feel it, changes your relationship to the work in ways I am still processing.

## The 47-file moment

Early in the [lib-pcb](https://github.com/exoreaction/lib-pcb) build, I hit a coordinate system problem. Bounding box calculations were returning dimensions twice the actual board size because documentation layers contained inflated coordinates. The fix required changes across parsers, validators, and rendering logic.

I made the mistake of delegating vaguely. Something like "refactor the coordinate handling to exclude documentation layers from bounding box calculations." The AI went to work. When it finished, 47 files had changed. The diff was enormous. I read through it for twenty minutes and realized I could not confidently say whether every change was correct. Some files I barely recognized. The AI had made decisions about scope, about which edge cases to handle, about how to restructure shared utilities, and I had not been part of any of those decisions.

The code compiled. The tests passed. But I did not understand what had happened to my own codebase.

That was the moment I learned the difference between delegation and abdication.

## Vague delegation versus strategic delegation

Vague delegation sounds like: "Refactor the coordinate system." It is the kind of instruction you might give a senior developer who understands the codebase deeply and shares your mental model of the architecture. The AI does not share your mental model. It has no model. It has pattern matching and the context you provide. When you delegate vaguely, you get a plausible interpretation of your intent, applied broadly and confidently, with no hesitation at the points where a human would pause and ask a clarifying question.

Strategic delegation is the opposite. It is small, explicit, and scoped. It sounds like this:

"Show me every file that references `BoundBox.getWidth()` in the rendering package."

"In `GerberParser.java`, change the layer filtering logic so documentation layers are excluded before bounding box calculation. Do not change any other file."

"Write a test that parses `test-german-manufacturer.gbr` and asserts the bounding box width is 216mm, not 432mm."

Three requests instead of one. Each one is verifiable. Each one leaves me in control of the architectural decision -- which files change, what the expected behavior is, where the boundary of the change sits. The AI handles execution. I handle scope and judgment.

This is not slower. It is faster, because I do not spend twenty minutes trying to reverse-engineer what happened. I know what happened because I directed each step.

## The architecture collapse

Here is what I did not expect. This way of working is what "architect" has always meant. An architect identifies the problem, decides what should change, specifies the desired outcome, and reviews the result. That is the job description. But in practice, architects have historically fallen into one of two failure modes.

Some stayed too abstract. They drew diagrams and wrote documents, but lost touch with the code. Their architectural decisions became disconnected from implementation reality because they were not close enough to see how the code actually behaved. Their guidance was theoretically sound and practically useless.

Others got pulled into implementation. They were too skilled to resist, or the team was too small, and they ended up writing code alongside everyone else. The architectural view dissolved into the details. They could see the current method clearly but lost sight of the system.

AI collapses that tension. You can direct implementation at the line-of-code level -- "change this method, add this test, restructure this class" -- without doing the implementation yourself. You stay close enough to the code to make informed decisions. You stay far enough from the typing to maintain the architectural view.

During lib-pcb, my working rhythm became something like this: I identify a problem or a gap. I ask the AI to explore the codebase and show me what is relevant. I decide what should change and how. I direct the AI to implement to my specification. I review the output. I direct the AI to write tests. I merge when satisfied.

Seven steps. Four are human judgment. Three are AI execution. I called this "directed synthesis" in an earlier post. But what it really is, I think, is what architecture was supposed to be all along.

## The identity question

I have been writing code since 1994. Thirty-two years. My identity as a professional is tangled up in the act of writing code. The satisfaction of a clean implementation. The flow state of debugging a complex problem by tracing through the logic line by line. The craft of it.

When the AI writes the code, am I still a developer?

I sat with that question longer than I want to admit. It is not a theoretical concern. It is a real discomfort that shows up on Tuesday afternoon when you realize you have been directing work for three hours and have not typed a single line of production code yourself.

The answer I arrived at is yes, but the reasoning matters. The architecture decisions are still mine. The judgment calls -- what to build, what to skip, which edge cases matter, which abstractions will hold and which will collapse under real-world usage -- are still mine. The domain understanding that tells me a 432mm bounding box is wrong for a board that should be 216mm, that is thirty years of experience doing its job. The AI does not have that. It cannot have that. It can write the parser, but it cannot know what a correct parse looks like for a file from a manufacturer that deviates from the specification in ways no documentation covers.

What shifted is not whether I am a developer. What shifted is what the word means. It used to mean someone who writes code. It now means someone who directs the creation of software systems, using every tool available, with the judgment and domain knowledge to ensure what gets built is correct.

## What "developer" means now

The traditional split was: managers decide what to build, developers decide how to build it. AI dissolves that boundary from the developer side. Experienced developers now work at the what-and-why level by default, because the how-level is handled by something that does it faster than they can.

This is not a demotion. It is the opposite. For thirty years, the highest-leverage work a developer could do was constrained by the fact that they also had to do the lowest-leverage work. You could see the right architecture, but you still had to type the implementation. You could spot the better approach, but switching to it cost weeks, so you stuck with the adequate one.

When implementation is cheap, you spend your time on the decisions that actually determine whether the software works. The what, the why, the boundary conditions, the verification strategy, the domain constraints. The work that was always the most important part of development, but that got buried under the volume of typing.

The word "developer" is not changing into something lesser. It is changing into what it probably should have meant all along.

---

*This post is part of the [AI-Augmented Development](/blog/category/ai-augmented-development/) series, exploring how thirty years of software experience intersects with AI-assisted development. All observations grounded in building [lib-pcb](https://github.com/exoreaction/lib-pcb), a 197,831-line PCB manufacturing library, in 11 days.*
