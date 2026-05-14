---
tags:
  - LinkedIn
  - Writing
date: 2026-04-06
---

# Quantum abstractions leak — IBM

*April 6, 2026 · [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7446873479620005888)*

**39 reactions · 5 comments · 3,368 views**

---

I spent Easter Monday running a quantum physics experiment on real IBM hardware.

Not a tutorial. An actual measurement designed to test a specific theoretical prediction.

It didn't work at first. Then it sort of worked. Then it finally worked — but only after we understood the machine well enough to stop fighting it.

Three things that tripped us up, in order:

1. We were on the wrong hardware.  
 IBM's open plan routes you to Heron r2 processors. What we needed was Eagle r3 (ibm_strasbourg).  
 Different coherence times, different error rates. Not obvious until the results came back looking like noise.

2. We needed to solve a subgraph matching problem by hand.  
 Eagle processors use a heavy-hex coupling map — each qubit connects to at most three neighbors. Our circuit needed a specific connectivity pattern. Finding it meant sitting down with the physical topology and calibration data and finding a layout that matched.

3. Twelve of our gate directions were wrong.  
 IBM's native two-qubit gate (ECR) is directional. Write a CNOT backwards relative to the coupling map and the transpiler silently adds SWAP chains to compensate. For twelve gates: circuit depth 2045 instead of 242. Eight times as deep. Coherence time obliterated.

We audited every edge. Rewrote the circuit. Depth dropped. The result landed exactly where the theory predicted.

No dramatic moment. Just a number on a screen that matched a prediction — earned through two hours of debugging hardware constraints.

The abstractions leak. Constantly. You cannot treat quantum processors as black boxes and expect meaningful results. The coupling map matters. The gate directions matter. The specific qubits you pick on a specific chip on a specific day matter.

It's closer to experimental physics than software engineering.

#QuantumComputing #IBMQuantum #Hardware #Experimentation

---

## Discussion

> **Totto** ↩: Full blogpost:  https://wiki.totto.org/blog/2026/04/06/the-abstractions-leak-a-day-with-ibm-quantum-hardware/

> **That jump from 2045 to 242 depth just by fixing gate directions is wild.**: That jump from 2045 to 242 depth just by fixing gate directions is wild.

> **Totto** ↩: Maximilien Frisch 
 It surprised me too, honestly. Twelve CNOTs pointing the wrong way against the native ECR direction — each one forces the transpiler to decompose and patch, and it cascades. You don't see it until the depth is 8x what it should be and your results are just noise. The lesson: audit the coupling map before writing the circuit, not after. 🙂

> **Really good! It is important to regularly de-hype by reporting about the reality - otherwise it is just cocktails and sunshine without reality touch base.**: Really good! It is important to regularly de-hype by reporting about the reality - otherwise it is just cocktails and sunshine without reality touch base.

> **Totto** ↩: Nikolay Tcholtchev 
Exactly. The hype creates the expectation that you run a circuit and get a clean result. The reality is that most of the time is spent  understanding why the result is wrong — and most of that "why" lives in the hardware, not the algorithm. That gap between expectation and reality is where most quantum projects quietly stall. Worth documenting honestly.

---

← [All LinkedIn posts](index.md)
