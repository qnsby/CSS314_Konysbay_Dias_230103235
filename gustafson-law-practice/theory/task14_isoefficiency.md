# Task 14 — Isoefficiency

For useful one-core work W and parallel time T_P, total overhead is T_o=P T_P−W. Then

`E=W/(P T_P)=1/[1+T_o/W]`.

Maintaining E=E₀∈(0,1) requires `W=[E₀/(1−E₀)] T_o(W,P)`.

In the ideal Gustafson family T_P=a+b and W=a+Pb. Thus T_o=(P−1)a=Θ(P) for fixed a>0, and W=Θ(P) is sufficient for a nonzero limiting efficiency. More exactly, solving E₀=(a+Pb)/[P(a+b)] gives b=a(E₀P−1)/[P(1−E₀)], approaching a constant as P grows.

Therefore the ideal family's asymptotic isoefficiency is Θ(P), with enough concurrent work. Pure fixed-b weak scaling approaches 1−α; it does not hold efficiency exactly constant at every finite P.

For C(P)=Θ(log P), overhead becomes Θ(P log P), and constant-efficiency work must grow at least Θ(P log P), assuming this growth does not change the cost model. Weak scaling W=Θ(P) is then insufficient. If a=0 and there is no overhead, efficiency is identically one and overhead imposes no nontrivial isoefficiency requirement. Critical-path constraints can still impose concurrency bounds.
