# Task 20 — Irregular graph workloads

In BFS, the active frontier changes at every level. A power-law graph's high-degree vertices create skew: equal vertex counts do not imply equal edge traversal work. Cross-partition edges require remote discovery messages, duplicate suppression, and synchronization; high diameter increases the number of dependent levels.

PageRank scans edges repeatedly, but destination updates are sparse, irregular and often remote. Hubs concentrate messages and create contention; convergence criteria can change iteration counts as the graph grows. Fixed vertices per worker therefore does not guarantee fixed edges, communication, or time per worker.

Dense matrix kernels have predictable blocks, regular reuse and efficient vectorized arithmetic. Graph traversal frequently has low arithmetic intensity, cache misses, latency-bound pointer/index access, and insufficient useful work per synchronization. Increasing graph size can change degree distributions and partition cuts rather than simply replicate an identical local kernel.

Partition by edges/work, use vertex cuts or hybrid partitions for hubs, batch messages, compress frontiers, and measure cut edges, frontier imbalance, iterations, and memory traffic. These can improve performance but do not guarantee constant α. Report input graph generation and topology as well as processor count to make a weak-scaling claim reproducible.
