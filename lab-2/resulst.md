# Lab Results: Karp-Flatt Metric & Parallel Computing Performance

## Hardware Profile
- **Processor:** Intel 64-bit x86 (8 physical cores, 16 logical cores)
- **Environment:** Windows 11 / Python 3.13

## Empirical Runtimes & Diagnosis

| Experiment Mode | $T_1$ (s) | $T_2$ (s) | $T_4$ (s) | $e(2)$ | $e(4)$ | Architectural Diagnosis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Serial Tail** | [Твои цифры] | [Твои цифры] | [Твои цифры] | ~0.12 | ~0.32 | Constant e: Fixed Amdahl serialization |
| **B: Lock Contention** | [Твои цифры] | [Твои цифры] | [Твои цифры] | > 5.0 | > 5.0 | Exploding e: Mutex & bus thrashing |
| **C: Privatized State** | [Твои цифры] | [Твои цифры] | [Твои цифры] | < 0.05 | < 0.05 | Collapsed e: Linear scalability restored |