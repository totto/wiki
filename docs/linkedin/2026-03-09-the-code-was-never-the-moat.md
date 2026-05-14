---
tags:
  - LinkedIn
  - Writing
date: 2026-03-09
---

# The Code Was Never the Moat

*March 9, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7436708903956135936)*

**28 reactions · 9 comments**

---

Bruce Perens — author of the Open Source Definition — just said "the entire economics of software development are dead."

He said this after a developer rewrote a 130-million-download Python library in five days using Claude. 1.3% textual similarity to the original. LGPL to MIT. Clean room implementation.    
   
He is half right.   
   
The economics of code as artifact are dying. When anyone can reimplement a library from its specification in days, the code itself stops being a moat.

But the economics of knowing what to build are stronger than ever. Domain expertise, architectural judgment, the ability to direct AI toward correct output rather than merely compiling output — those economics are not dead. They are amplified.

When anyone can produce code, the scarce resource is knowing what code to produce.

Full reflection on the blog: https://lnkd.in/e-5JEfW2

---

## Discussion

> **The challenge is never the first implementation. The challenge is ongoing maintenance and development. 
Folks who collaborate will always outperform those who do not. 
Not collaborating is a waste of tokens and precious human time.
The "clean room" reimplementation is likely to miss edge cases and behavior that wasn't fully specified but is relied on.
And that's before we get to answer the question whether the result of such an output truly is clean room (the model clearly has seen the sources before) or still a derivative work or maybe doesn't meet the copyright threshold at all. **: The challenge is never the first implementation. The challenge is ongoing maintenance and development. 
Folks who collaborate will always outperform those who do not. 
Not collaborating is a waste of tokens and precious human time.
The "clean room" reimplementation is likely to miss edge cases and behavior that wasn't fully specified but is relied on.
And that's before we get to answer the ques...

> **Totto** ↩: Lars Marowsky-Brée You're reinforcing the thesis from the other end. The first implementation proves the specification was
 complete enough to be replicated. Ongoing maintenance is where the knowledge that wasn't in the specification accumulates — edge cases, silent requirements, "why we didn't do it that way." That compounded maintenance knowledge is exactly what can't be extracted from observ...

> **Wait til they do it to get GPL3 code under an MIT licence. All those libraries will be available without having to open source commercial code using it.**: Wait til they do it to get GPL3 code under an MIT licence. All those libraries will be available without having to open source commercial code using it.

> **Totto** ↩: Ray Gardener Fair points, especially on maintenance — that's where most software cost lives. The 5-day rewrite is striking, but you're right that the long tail matters more. What I'm less sure about: whether AI changes the maintenance economics too. Bug fixes, edge case discovery, documentation — these also accelerate. The collaboration question is the one I keep coming back to. Open source doe...

> **Ray Gardener**: Ray Gardener Wait til they do it to get closed source software X from big company Y reimplemented under licence Z (e.g. X = Microsoft Words, Y = Microsoft, Z = GPL3). Copyright on software may seem shaky, and I expect toward software patenting, including a severe push for "first to file" instead of searching prior art, in a way to manage intellectual property...

> **This was definitely not a clean room implementation - the original source code was in the training data.**: This was definitely not a clean room implementation - the original source code was in the training data.

> **Totto** ↩: Vladimir Panov 
Fair — clean room is the wrong frame when the training data includes the source.

 The economic question is separate though: even if the IP argument is unsettled, Perens' core claim is about the marginal cost of generating working code dropping to near zero. That holds regardless of where the model learned it. The interesting question shifts to maintenance, differentiation, and ...

---

← [All LinkedIn posts](index.md)
