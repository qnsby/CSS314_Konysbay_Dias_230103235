# Task 09 — Composite serial overhead

Treat A (2%) and B (6%) as non-overlapped, non-scalable elapsed phases, as intended in the exercise. Then α=.02+.06=.08, parallel fraction=.92.

| P | Serial contribution | Parallel contribution .92P | Speedup | Efficiency |
|---:|---:|---:|---:|---:|
|512|.08|471.04|471.12|.92015625|
|2048|.08|1884.16|1884.24|.9200390625|

Communication is counted here as a fixed overhead fraction by assumption. In a real implementation broadcast and boundary exchange need not be serial CPU work or remain at 6% as P grows; explicit parallel-only overhead should use the Task 12 denominator model.
