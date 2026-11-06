# Task 12 — Explicit communication penalty

Let a be useful serial time, b useful computation time per worker under ideal weak scaling, and C(P) additional parallel-only overhead with C(1)=0. Then

`T_P=a+b+C(P)`, `T₁(P)=a+Pb`.

Writing α₀=a/(a+b) and c(P)=C(P)/(a+b),

`S_real(P)=[P−α₀(P−1)]/[1+c(P)]`.

The serial reference excludes parallel-only messages. A naive subtraction of C from ideal speedup mixes time units and ratios.

For a tree collective, C(P)=λ log₂P gives efficiency asymptotically Θ(1/log P), when λ>0 and α₀<1. For C(P)=λ(√P−1), efficiency is Θ(P^(−1/2)). Runtime therefore does not remain fixed. These are illustrative cost functions, not universal measurements.

If instead communication replaces useful computation within an externally fixed runtime budget, useful b must shrink as C grows. That is a different workload policy and requires recalculating the numerator as well.
