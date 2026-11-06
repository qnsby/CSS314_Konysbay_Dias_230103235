# Task 23 — Statistical definitions and fit interpretation

There are 80 measured runs: P=1,…,16 with five independent fresh-Pool repetitions each. `results.csv` preserves individual wall-clock times. `summary.csv` reports mean speedup, sample standard deviation, standard error, and runtime statistics.

For each run i, Sᵢ=T_serial,i(Pk)/T_parallel,i(Pk). We fit the required Gustafson curve Sᵢ=Pᵢ−α(Pᵢ−1)+εᵢ with its theoretical intercept fixed, minimizing squared residuals over all raw observations:

`alpha_hat = sum[(P_i−1)(P_i−S_i)] / sum[(P_i−1)^2]`.

The five equal-size groups make raw-observation OLS equivalent to fitting group means with equal weights. Standard deviations use n−1; plotted standard errors are std/√5. They describe spread/uncertainty of speedup estimates, not runtime units or 95% confidence intervals. Mean of per-run ratios is deliberately used instead of a ratio of runtime means.

The observed fitted α is about **1.023794**, outside [0,1]. A physical constrained least-squares fit would reach boundary α=1, predicting S=1 throughout, but would still miss measured sub-unit speedups. We retain the unconstrained result rather than presenting it as a physical serial-time fraction. `fit.json` records both the raw estimate and its projection.

The fixed intercept predicts S(1)=1 whereas measured mean S(1)≈0.170891, because a Pool with one worker still pays process startup. P=1 adds residual error but has zero leverage on α. The fit's negative slope is consequently a visible **model failure**, not evidence that useful parallel work is negative. Do not extrapolate the fitted curve to large P.

End-to-end Pool startup dominates this short workload. A persistent-worker experiment or larger k could study amortization, but would answer a different timing question and should be saved as a separate dataset. Randomized configuration order reduces systematic ordering effects but cannot eliminate OS noise or thermal drift.
