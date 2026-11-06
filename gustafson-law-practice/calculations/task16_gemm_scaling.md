# Task 16 — Dense matrix multiplication

Ignoring communication, T_P≈cN³/P. Keeping it equal to cN₀³ yields `N(P)=N₀P^(1/3)`.
Memory for three dense matrices is proportional to N², hence total memory grows as P^(2/3), and ideal distributed memory per processor decreases as P^(−1/3).

| P | N/N₀ | Total memory/M₀ | Work/W₀ |
|---:|---:|---:|---:|
|1|1|1|1|
|8|2|4|8|
|64|4|16|64|
|512|8|64|512|
|4096|16|256|4096|

Rounding N to integers slightly changes work. A memory-filling policy N∝√P instead makes work∝P^(3/2) and compute time∝√P; that is memory-bounded scaling, not fixed-time scaling. Communication and minimum local tile sizes restrict the ideal formula at large P.
