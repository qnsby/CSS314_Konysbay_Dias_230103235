# Task 10 — 3D memory ceiling

Let b be total bytes stored per grid cell, including all fields, time levels and auxiliary arrays, and H(P,N) extra halo/runtime memory. With P nodes of 32 GB each,

`bN³+H(P,N)≤32·10⁹ P`, so ignoring H,

`N_max(P)=floor((32·10⁹ P/b)^(1/3))`.

The problem does not specify b, so a unique numerical dimension cannot be inferred. For an explicit illustrative single-float64-field assumption b=8 bytes and H=0:

| Nodes | Aggregate decimal capacity | Cells available | Maximum cubic N |
|---:|---:|---:|---:|
|64|2048 GB|256,000,000,000|6349|
|512|16384 GB|2,048,000,000,000|12699|

Increasing nodes eightfold doubles the continuous cube dimension. More fields reduce N by b^(−1/3); halos reduce feasible size further. If GB actually means GiB, replace 10⁹ by 2³⁰. Distribution must also satisfy each node's local memory cap, so these are aggregate upper bounds, not allocation guarantees.
