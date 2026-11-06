# Gustafson's Law & Weak Scaling — Practice Tasks 01–25

Student: Dias Konysbay, 230103235. This folder contains theory, worked calculations, executable simulations, local measurements, regression, and plots for the **Gustafson Law Practice Tasks** sheet.

## How to use this repository

All answers are written in English and follow the task sheet. The index below links to each of the 25 tasks. Raw measurements are stored in `benchmarks/results.csv`, and generated plots are in `plots/`. To reproduce the results, install the dependencies and run the commands below. Rerunning the benchmark overwrites the data; afterward, regenerate the plots and update the numerical conclusions in the analysis documents.

## Mathematical guide

Gustafson: `S_G(P)=P−α(P−1)` and `E_G=1−α+α/P`, where α is the serial fraction of **parallel elapsed time**. Amdahl: `S_A(P)=1/[s+(1−s)/P]`, where s is the serial fraction of **one-core elapsed time** for a fixed workload. Identical numeric fractions do not generally describe the same job.

For identical useful serial time a and one-core parallelizable work b, `α=P s/[1+(P−1)s]`. Ideal weak scaling holds useful work per worker constant; for work Θ(Nᵈ), dimension grows as P^(1/d). With parallel-only communication C(P), use `S=(a+Pb)/(a+b+C(P))` rather than counting messages as useful serial work.

Choose weak scaling when increased resources should buy a larger simulation, more samples, or higher resolution within a time budget. Partition work rather than just element counts; maintain independent random streams, balanced subdomains, and bounded communication per worker. Use strong scaling when a fixed job must finish sooner. Check memory, dependency depth, network topology and synchronization before assuming that constant elements per worker imply constant runtime.

## Run commands

The empirical telemetry collector targets Windows/PowerShell. The simulator and fitting scripts are portable Python.

```powershell
python -m pip install -r requirements.txt
python benchmarks/simulator.py --max-p 65536 --alpha .001 .04 .08 .20
python benchmarks/weak_scale_bench/run.py --k 1750000 --runs 5
python benchmarks/fit_gustafson.py
```

The benchmark uses every process count 1–16 on the measured host and five independent fresh-Pool repetitions per count, with a shuffled schedule. Each repeat compares the same scaled job sequentially and in parallel. Pool creation, worker imports, IPC and shutdown are included in parallel wall time. The stored 80 runs all pass numerical equality checks.

## Experimental synthesis

On this Intel i7-11800H laptop (8 physical cores / 16 threads), mean scaled speedup grows from 0.170891 at P=1 to 0.664462 at P=8 and 0.795178 at P=16, remaining below one. Mean parallel runtime rises from 0.326109 s to 0.641980 s and 1.115167 s respectively. These end-to-end measurements demonstrate startup costs and imperfect weak scaling for the chosen short kernel, rather than a universal limit on multiprocessing.

Least-squares fitting yields α=1.023794 with group-mean RMSE=0.354622. This is outside the model's physical range. The unconstrained curve is displayed transparently; it must not be interpreted as a valid serial fraction or extrapolated. The fixed S(1)=1 assumption fails because one-worker Pool overhead is measurable. The same-number Amdahl curve is included for the requested comparison, with this limitation stated explicitly.

Each task's two main arrays require 28 MB, exceeding per-core L2 and shared L3. Memory traffic, SMT resource sharing and launch/import overhead are plausible contributors. Thermal throttling, active memory channels, and NUMA effects were not measured, so no causal claim is made about them. A larger kernel or persistent-worker variant is a useful separate experiment, not a reason to alter the raw data.

## Task index

| Task | Artifact |
|---:|---|
|01|[Scaling foundations](theory/task01_scaling_models.md)|
|02|[First-principles derivation](theory/task02_derivation.md)|
|03|[Serial-fraction reference frames](theory/task03_serial_invariance.md)|
|04|[Asymptotic limits](theory/task04_asymptotic_limits.md)|
|05|[Historical nCUBE reconstruction](theory/task05_historical_ncube.md)|
|06|[Parametric table](calculations/task06_parametric_table.md), [numeric log](calculations/task06_numeric_log.csv)|
|07|[Tolerable serial overhead](calculations/task07_tolerable_serial.md)|
|08|[Amdahl–Gustafson divergence](calculations/task08_cross_divergence.md)|
|09|[Composite phases](calculations/task09_multicomponent.md)|
|10|[Memory ceiling and missing-parameter assumption](calculations/task10_memory_growth.md)|
|11|[Sun–Ni comparison](theory/task11_sun_ni_comparison.md)|
|12|[Communication penalty model](theory/task12_communication_penalty.md)|
|13|[Algorithmic failure cases](theory/task13_failure_cases.md)|
|14|[Isoefficiency](theory/task14_isoefficiency.md)|
|15|[Energy scaling](theory/task15_energy_scaling.md)|
|16|[GEMM dimensions](calculations/task16_gemm_scaling.md)|
|17|[Stencil surface/volume analysis](calculations/task17_stencil_scaling.md)|
|18|[N-body methods](analysis/task18_nbody_scaling.md)|
|19|[Monte Carlo and reductions](analysis/task19_monte_carlo.md)|
|20|[Graph processing](analysis/task20_graph_processing.md)|
|21|[Simulator](benchmarks/simulator.py), [generated CSV](benchmarks/simulation.csv), [PDF](plots/simulation.pdf), [PNG](plots/simulation.png)|
|22|[Benchmark implementation](benchmarks/weak_scale_bench/run.py), [run instructions](benchmarks/weak_scale_bench/README.md)|
|23|[80 raw measurements](benchmarks/results.csv), [summary](benchmarks/summary.csv), [fit script](benchmarks/fit_gustafson.py), [fit metadata](benchmarks/fit.json), [statistical interpretation](analysis/task23_regression_method.md)|
|24|[Hardware audit](analysis/task24_hardware_audit.md), [telemetry](benchmarks/telemetry.json), [additional cache telemetry](benchmarks/cache_audit.json), [vector PDF](plots/scaling_comparison.pdf), [400-dpi PNG](plots/scaling_comparison.png)|
|25|This README: mathematical guide, empirical synthesis, commands and artifact index|

Dependencies are in [requirements.txt](requirements.txt). Python cache and virtual-environment exclusions are in [.gitignore](.gitignore).

## Sources and reproducibility

Historical claims: [Gustafson's original 1988 account](https://users.cs.utah.edu/~hari/teaching/paralg/Gustafson88.pdf). Memory-bounded model: [Sun and Ni, 1993](https://www.cs.iit.edu/~scs/psfiles/Sun_and_Ni_JPDC1993.pdf). CPU capability comparison: [Intel specifications](https://www.intel.com/content/www/us/en/products/sku/213803/intel-core-i711800h-processor-24m-cache-up-to-4-60-ghz/specifications.html). Measurements and machine configuration come from local runs, not these references.

The Git repository is initialized locally with task-sized commits. No remote repository was configured or uploaded. To integrate with your designated personal repository, copy this dedicated folder into it (excluding the nested `.git` directory) and commit there, or configure a remote for this repository according to your course's submission workflow.
