# Task 17 — Global versus local surface-to-volume ratio

For one stencil iteration, work∝N³ and external domain surface∝N². Constant ideal compute time with P processors requires N=N₀P^(1/3). The **global exterior** surface/work ratio is 1/N∝P^(−1/3), so that ratio improves.

Distributed halo traffic is different. Assume a balanced 3D processor grid with P=q³ and cubic local domains of side n=N/q. Under weak scaling n=N₀ is constant. Each worker computes Θ(n³) updates and exchanges Θ(6n²) face values. Thus local communication/computation≈6/n remains constant; aggregated internal boundaries are Θ(Pn²), not Θ(N²).

For strong scaling at fixed N, n=N/P^(1/3), so the local ratio grows as P^(1/3)/N. Slab decomposition can give worse weak scaling: thickness N/P shrinks while faces grow, making the ratio grow as P/N∝P^(2/3).

Therefore the exercise's improving global ratio does not prove improving distributed communication. With 3D decomposition ideal weak scaling preserves the ratio; network contention, latency and global reductions may degrade actual runtime.
