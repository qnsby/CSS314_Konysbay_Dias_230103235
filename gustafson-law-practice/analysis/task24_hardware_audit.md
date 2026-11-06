# Task 24 — Hardware audit and discrepancy analysis

## Observed environment

The full machine-readable source is [telemetry.json](../benchmarks/telemetry.json), captured locally with Windows CIM, Python and NumPy.

| Item | Observation |
|---|---|
| Laptop | Acer Nitro AN515-57 |
| CPU | Intel Core i7-11800H @ 2.30 GHz model string |
| Execution resources | 8 physical cores, 16 logical threads |
| OS | Windows 11, build 26300 |
| Python / NumPy | 3.13.13 / 2.5.3 |
| L1 | Additional CIM cache audit reports two L1 entries of 384 and 256 KiB aggregate; their types were not captured |
| L2 | 10240 KiB total; 1280 KiB/core if evenly divided |
| L3 | 24576 KiB = 24 MiB shared |
| Memory modules | 2 × 8 GiB; both configured at 2667 MT/s according to CIM |
| OS-visible memory | 16,931,676,160 bytes, approximately 15.77 GiB |
| Process creation | spawn |

The additional [cache audit](../benchmarks/cache_audit.json) preserves firmware cache entries: Win32_CacheMemory Level=3 means L1, Level=4 means L2, and Level=5 means L3. L1 instruction/data types and active cache-miss counters were not captured, so the two L1 entries are left unlabeled. Intel documents a maximum of two memory channels for this CPU; this is a controller capability, not proof that both channels are active. CIM reports two module/controller locators, but those firmware strings do not establish interleaving or measured bandwidth. Active memory-channel configuration remains unverified. Reference: [Intel processor specifications](https://www.intel.com/content/www/us/en/products/sku/213803/intel-core-i711800h-processor-24m-cache-up-to-4-60-ghz/specifications.html).

## Measured behavior

| P | Mean serial runtime (s) | Mean parallel runtime (s) | Mean per-run speedup |
|---:|---:|---:|---:|
|1|0.055809|0.326109|0.170891|
|8|0.425137|0.641980|0.664462|
|16|0.885331|1.115167|0.795178|

These are fresh-Pool end-to-end measurements over five repeats, with k=1,750,000 float64 elements per task. All 80 numerical comparisons passed. More processes give more work but parallel runtime does not remain flat. SMT cannot double vector execution units or memory bandwidth; Windows process launch and imports also grow with concurrency.

The two-array footprint is 28 MB (26.70 MiB) per task, exceeding one core's L2 and even the shared L3. NumPy temporaries add allocations and memory traffic. At 16 tasks the two-array estimate reaches 448 MB, so cache reuse and DRAM bandwidth are plausible limits, but no bandwidth-saturation measurement was made.

The OLS α≈1.023794 is outside the physical range, as explained in [Task 23](task23_regression_method.md). Consequently the same-number Amdahl curve is an algebraic comparison outside its physical parameter assumptions. Equal numeric α and s are already different reference frames even when in range.

Thermal throttling, actual CPU frequencies, and NUMA placement were not instrumented. Laptop power/temperature changes and background activity could contribute to variance, but cannot be claimed as observed causes. This single-CPU laptop was not tested across NUMA boundaries; a NUMA explanation would require topology and remote-memory evidence.

## Plot artifacts

[Vector PDF](../plots/scaling_comparison.pdf) and [400-dpi PNG](../plots/scaling_comparison.png) show ideal S=P, unconstrained Gustafson OLS, measured means ± standard error, and Amdahl with the same numeric fraction. A second panel magnifies the measured scale so the ideal line does not hide error bars. Raw measurements are preserved without normalization or fabricated corrections.
