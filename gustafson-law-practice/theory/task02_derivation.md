# Task 02 — Derivation from first principles

1. Observe a scaled workload on P identical processors. Normalize its elapsed time to T_P=s+p=1.
2. s is elapsed serial time; p is elapsed time in the ideally balanced parallel region. Neither variable is a processor count.
3. The serial region performs s units of one-processor work.
4. During the parallel region P processors each perform p units, so total parallelizable work is Pp.
5. Running the **same scaled workload** on one processor would take T₁=s+Pp, assuming identical per-core performance and no parallel overhead.
6. Speedup is S=T₁/T_P=(s+Pp)/(s+p)=s+Pp.
7. Let α=s/(s+p)=s. Then p=1−α.
8. Substitute: S=α+P(1−α)=P−α(P−1).

Checks: S(1)=1; α=0 gives S=P; α=1 gives S=1. Efficiency is E=S/P=1−α+α/P.

These equations assume that the serial reference performs the same useful work and that communication is absent or explicitly modeled. Counting communication as useful serial work in T₁ can inflate speedup.
