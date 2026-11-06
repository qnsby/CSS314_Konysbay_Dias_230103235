# Task 08 — Divergence at 128 processors

With one-core s=.08, S_A=1/[.08+.92/128]=1/.0871875=11.4695340502.

Using the same numeric parallel-runtime fraction α=.08, S_G=128−.08·127=117.84.

Difference: 106.3704659498; ratio S_G/S_A=10.274175.
Taking Amdahl as the denominator, percentage increase is **927.4175%**.
Taking Gustafson as the denominator, the gap is approximately **90.2668584%**.
The denominator must be specified because “percentage discrepancy” is ambiguous.

These are different scaling experiments. If the Amdahl workload is held fixed, its matching parallel fraction is α=128·.08/[1+127·.08]=10.24/11.16≈.917563; Gustafson then yields the same 11.469534 speedup. There is no physical crossover of inconsistent fractions.
