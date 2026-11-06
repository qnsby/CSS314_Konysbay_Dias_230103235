# Task 11 — Memory-bounded speedup

Let s denote the baseline one-core serial fraction and G(P) the multiplier of parallelizable *work* permitted by expanded memory. A useful normalized Sun–Ni form is

`S_MB(P)=[s+(1−s)G(P)]/[s+(1−s)G(P)/P]`.

G(P)=1 recovers Amdahl. G(P)=P recovers the algebraic Gustafson expression s+P(1−s), because the normalized denominator is then one. The use of s here is the baseline fraction of the unexpanded problem; the scaled one-core fraction changes with G.

Memory capacity and work need not scale identically. If work∝Mʳ and aggregate memory grows by P, then G(P)=Pʳ, ignoring replication and communication. For r>1 this permits more than linearly growing work, with growing parallel runtime, and may yield a higher speedup than a constant-time Gustafson prediction. For r<1, memory limits, replicated data, or insufficient work growth can yield a smaller speedup. Overhead and imbalance lower achievable performance further.

Speedup is a ratio relative to the *same expanded job*. A larger memory-bounded speedup does not by itself imply more jobs per second or constant time to solution.

Primary reference: [Sun and Ni, Scalable Problems and Memory-Bounded Speedup, JPDC 19, 1993](https://www.cs.iit.edu/~scs/psfiles/Sun_and_Ni_JPDC1993.pdf).
