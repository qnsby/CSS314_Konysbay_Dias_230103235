# Task 13 — Two failure cases

## Direct all-pairs interaction with N∝P particles

Work is Θ(N²). Equal distribution yields T_compute=Θ(N²/P). If N=N₀P, time grows as Θ(P), even before communication. Each worker also needs remote particles or replicated global data, increasing traffic or memory. Constant particles per worker is not constant interactions per worker. Fixed compute time instead requires N∝√P, subject to communication costs.

## Level-synchronous BFS on a path

A path of N vertices has Θ(N) work but also Θ(N) dependent BFS levels from an endpoint. Each level exposes only one new vertex, so additional workers cannot keep busy. With N∝P, useful elapsed work remains Θ(P), rather than constant. A distributed implementation also pays a collective/termination synchronization per level; a tree collective can add Θ(N log P) latency.

Both examples violate fixed parallel time for distinct reasons: the first increases arithmetic work per processor; the second has a growing critical path and insufficient available parallelism. Gustafson is a conditional model, not a guarantee that adding data creates usable parallel work.
