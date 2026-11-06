# Task 06 - Parametric speedup, alpha=0.04

S(P)=0.96P+0.04; E(P)=0.96+0.04/P.

| P | S(P) | E(P) | Efficiency (%) |
|---:|---:|---:|---:|
|16|15.40|0.962500000000|96.250000000|
|64|61.48|0.960625000000|96.062500000|
|256|245.80|0.960156250000|96.015625000|
|1024|983.08|0.960039062500|96.003906250|
|4096|3932.20|0.960009765625|96.000976562|
|16384|15728.68|0.960002441406|96.000244141|

Efficiency decreases monotonically from 96.25% at P=16 toward 96%. The decline is only 0.249755859 percentage points over the displayed range. It does not decay toward zero; the excess alpha/P vanishes. Scaled speedup remains linear.