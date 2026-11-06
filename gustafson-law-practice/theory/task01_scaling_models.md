# Task 01 — Strong and weak scaling

Let W be useful work, P the processor count, and T(P,W) runtime.

| Model | Held constant | What grows | Ideal runtime |
|---|---|---|---|
| Amdahl (1967) | W=W₀ | P | a+b/P |
| Gustafson (1988) | a target runtime | parallelizable work | a+b₀ |

For Amdahl, a is fixed serial time and b is fixed parallelizable one-core time.
With s=a/(a+b), S_A=1/[s+(1−s)/P]. As P→∞, problem dimension stays fixed and speedup tends to 1/s for s>0.

For ideal weak scaling, W_parallel(P)=P W_parallel(1), hence parallel computation per processor remains constant. Serial work need not grow. The total useful work is a+P b₀ in time a+b₀. As P→∞, work grows without bound while runtime remains bounded in this ideal model.

Problem *dimension* is not generally proportional to P: if work is Θ(Nᵈ), constant compute time requires N∝P^(1/d). Linear growth in elements applies only when work is linear in elements. Real communication, imbalance, memory bandwidth and serial preprocessing can invalidate fixed time.

The engineering questions differ: Amdahl asks how quickly an existing job finishes; Gustafson asks how much larger a job fits the same time budget. Neither law contradicts the other.
