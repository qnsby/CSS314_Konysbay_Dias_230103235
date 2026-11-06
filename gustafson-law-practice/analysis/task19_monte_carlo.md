# Task 19 — Monte Carlo and reduction trees

With k independent paths per worker and average cost c per path, useful compute time is b=ck and total samples Pk. Independent PRNG streams avoid a shared random-number lock; deterministic seed derivation from a global seed and stream index can be local. Poor stream splitting creates correlations, a correctness issue even if scaling looks ideal.

Nonzero overhead includes input loading, stream initialization, worker launch, scheduling, final reduction, and output serialization. A root that collects every worker sequentially has O(P) message handling; a balanced tree reduces critical-path reduction depth to ceil(log₂P).

With useful serial setup a and per-level reduction latency λ, an explicit model is

`S(P)=(a+Pb)/(a+b+λ ceil(log₂P))`.

For illustration a=.01 s, b=1 s and λ=.001 s give S(1024)=1024.01/1.02≈1003.9314, versus overhead-free S=1024.01/1.01≈1013.8713. These are modeled numbers, not empirical timings.

Tree reduction improves the O(P) bottleneck but does not preserve asymptotically constant runtime for fixed k and positive λ. Reducing infrequently or increasing k amortizes collective latency. Outputting every path rather than only statistics can dominate both communication and storage.
