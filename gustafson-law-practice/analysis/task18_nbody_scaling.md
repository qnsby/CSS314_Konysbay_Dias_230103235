# Task 18 — Direct and tree-code particle scaling

Direct interactions cost cN². Fixed ideal compute time requires N²/P=N₀², hence N=N₀√P. Scaling N linearly with P instead increases compute time linearly.

For balanced Barnes–Hut, average work is cN ln N. Fixed ideal compute time requires N ln N=P N₀ ln N₀. Let A=P N₀ ln N₀. Then N=exp(LambertW(A))=A/LambertW(A), asymptotically Θ(P/log P) for fixed N₀>1. This is neither exactly linear in P nor the direct method's square-root law. Pathological trees can violate the average complexity assumption.

The serial fraction cannot be determined from these complexities alone. If serial overhead is constant a and parallel compute time b is constant, α=a/(a+b) stays constant for either method. If direct initial setup takes Θ(N), α grows with √P unless setup is parallelized. A serial Θ(N log N) tree build grows as Θ(P) under the fixed-compute tree-code policy, driving α toward one. Parallel/distributed tree construction changes this conclusion.

Direct methods also incur particle exchange or replicated memory; tree codes add irregular traversals, load imbalance and remote tree-node access. These algorithm-dependent costs determine the actual serial/parallel ratio and must be measured rather than inferred solely from the big-O kernel cost.
