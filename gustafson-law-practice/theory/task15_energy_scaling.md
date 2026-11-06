# Task 15 — Energy under fixed elapsed time

Interpret P_idle as each powered node's static power and P_active as **additional** dynamic power at full activity. Let normalized serial duration α and parallel duration 1−α sum to a common elapsed time T. All P nodes remain powered; during the serial phase only one computes.

`Energy_P=T[P·P_idle + P_active(α+P(1−α))]`.

The one-node, smaller reference job in the same time consumes `Energy_1=T(P_idle+P_active)`. Thus

`Energy_P/Energy_1=[P·P_idle+S_G(P)P_active]/(P_idle+P_active)`.

Useful work grows by S_G(P), so energy per unit useful work is `T[P·P_idle/S_G(P)+P_active]`. Its asymptotic static contribution is T·P_idle/(1−α), for α<1. Total energy rises approximately linearly although elapsed time is unchanged.

For the **same expanded workload**, one core instead runs S_G(P)T seconds, so its energy is S_G(P)T(P_idle+P_active). This is a different comparison from identical wall-clock time. Power gating, idle spinning, turbo frequency, memory/network power and cooling modify these ideal equations. If P_active means total active power, replace the incremental term by P_active−P_idle.
