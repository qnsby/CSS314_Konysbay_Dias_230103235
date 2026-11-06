# Task 03 — Reference frames resolve the paradox

For a particular workload let serial work take a seconds and parallelizable work b seconds on one processor. Then

`s_A=a/(a+b)`, while `α_G=a/(a+b/P)`.

Eliminating a/b gives

`α_G=P s_A/[1+(P−1)s_A]`, and `s_A=α_G/[P−α_G(P−1)]`.

Using this transformed fraction, Amdahl and Gustafson yield exactly the same speedup for the same workload. Substituting the same numeric fraction into both formulas generally describes different workloads.

In an ideal weak-scaling family b(P)=P b₀ and a is constant. Thus α_G=a/(a+b₀) stays constant but s_A(P)=a/(a+P b₀) falls as 1/P. A fixed serial *duration* therefore does not imply a fixed serial *fraction* of the expanding one-core job.

There is no removal of serial overhead: if a(P), communication, or synchronization grows, the constant-α premise may fail. Gustafson measures the fraction in the parallel-runtime frame; it does not prove that fraction is invariant for arbitrary algorithms.
