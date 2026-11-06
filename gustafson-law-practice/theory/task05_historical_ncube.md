# Task 05 — Sandia's 1024-processor experiment

The 1988 Sandia work used a 1024-processor hypercube (the nCUBE setting identified in the task). Gustafson's contemporaneous account reports scaled speedups of 1021 for beam stress/conjugate gradients, 1020 for surface-wave finite differences, and 1016 for fluid flow/flux-corrected transport. These are application-specific findings, rather than a universal machine speedup.

If 0.4% were a fixed-workload one-core serial fraction, Amdahl's ceiling would be 250 and S_A(1024)=1/(.004+.996/1024)≈201.0998. But the small fractions discussed in the experiment were measured in the parallel-runtime frame while the parallel problem expanded.

For illustration α=.004 instead gives S_G(1024)=1024−.004·1023=1019.908. This illustrative value is not a replacement for any of the three reported results. Its equivalent one-core serial fraction is .004/1019.908≈0.000003922.

The experiment supports a different workload policy: use more processors for larger useful calculations within a time budget. It does not disprove Amdahl's algebra or establish linear scaling for communication-heavy programs.

Source: [Gustafson, Reevaluating Amdahl's Law, CACM 31(5), 1988](https://users.cs.utah.edu/~hari/teaching/paralg/Gustafson88.pdf). The task also refers to the related Gustafson–Montry–Benner application study.
