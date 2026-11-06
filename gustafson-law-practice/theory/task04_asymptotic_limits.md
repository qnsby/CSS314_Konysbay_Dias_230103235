# Task 04 — Efficiency limits

For fixed α∈[0,1], E_G(P)=1−α+α/P. Since lim(P→∞)1/P=0,

`lim E_G=1−α`.

For 0<α≤1, dE_G/dP=−α/P²<0: efficiency decreases toward a positive floor when α<1, even though speedup grows linearly. At α=1 the limit is zero; at α=0 efficiency is identically one.

Amdahl efficiency is E_A(P)=1/[P s+(1−s)]. For every fixed s>0 the denominator tends to infinity, so lim E_A=0. If s=0, E_A=1 for all P and the limit is one.

The limits use distinct invariants: fixed parallel-runtime α versus fixed one-core s. If α depends on P, its limit must be supplied before asserting a constant efficiency floor.
