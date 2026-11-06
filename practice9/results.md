# Lab Results Variant B: Scalability Diagnostics

## Hardware Profile
- **Processor:** Intel 64-bit x86 (8 physical cores, 16 logical cores)
- **Environment:** Windows 11 / Python 3.13

## Empirical Measurements

| Configuration | $T_1$ (s) | $T_2$ (s) | $T_4$ (s) | $T_8$ (s) | $S_8$ | $e(2)$ | $e(8)$ | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Micro (k=1)** | 30.542 | 32.601 | 39.742 | 35.350 | 0.86x | 1.135 | 1.180 | Master dispatch serialization |
| **B: Queue Choke** | 3.199 | 5.160 | 5.292 | 5.492 | 0.58x | 2.250 | 1.834 | IPC lock contention explosion |
| **C: Buffered Batch** | 0.859 | 0.605 | 0.365 | 0.357 | 2.40x | 0.410 | 0.333 | Amortized synchronization |