"""Task 22/23: five independent fresh-Pool measurements at each P."""
import argparse
import csv
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def kernel(task):
    index, k = task
    x = np.linspace(index, index+1, k, dtype=np.float64)
    y = np.sin(x*8)**2 + np.cos(x/5)**2
    return float(y.sum()), os.getpid()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--k', type=int, default=1_750_000)
    parser.add_argument('--runs', type=int, default=5)
    args = parser.parse_args()
    if args.k < 1 or args.runs < 5:
        parser.error('k must be positive; at least five runs are required')
    command = "[pscustomobject]@{cpu=(Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,L2CacheSize,L3CacheSize);memory=(Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity,Speed,ConfiguredClockSpeed,DeviceLocator,BankLabel);system=(Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory,Model)} | ConvertTo-Json -Depth 5"
    telemetry = json.loads(subprocess.check_output(['powershell','-NoProfile','-Command',command], text=True))
    telemetry.update(platform=platform.platform(), python=sys.version, numpy=np.__version__,
                     logical_concurrency=os.cpu_count(), parent_pid=os.getpid(),
                     timestamp=time.strftime('%Y-%m-%dT%H:%M:%S%z'), k=args.k,
                     start_method=mp.get_start_method(),
                     timing='Fresh Pool creation through join; serial baseline for the identical scaled workload',
                     thermal_counters='not measured', numa_topology='not measured', memory_channels='not directly measured')
    counts = list(range(1, os.cpu_count()+1))
    schedule = [(p, r) for p in counts for r in range(1,args.runs+1)]
    random.Random(230103235).shuffle(schedule)
    telemetry['schedule'] = schedule
    telemetry['workers'] = []
    with (ROOT/'benchmarks/results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['P','run','k','elements','T_serial','T_parallel','speedup','match'])
        writer.writeheader()
        for p,r in schedule:
            tasks=[(i,args.k) for i in range(p)]
            start=time.perf_counter()
            serial=list(map(kernel,tasks))
            ts=time.perf_counter()-start
            start=time.perf_counter()
            with mp.Pool(p) as pool:
                parallel=pool.map(kernel,tasks,chunksize=1)
            tp=time.perf_counter()-start
            match=all(math.isclose(a[0],b[0],rel_tol=1e-12) for a,b in zip(serial,parallel))
            if not match:
                raise RuntimeError('Numerical result mismatch')
            writer.writerow(dict(P=p,run=r,k=args.k,elements=p*args.k,T_serial=ts,T_parallel=tp,speedup=ts/tp,match=match))
            f.flush()
            telemetry['workers'].append(dict(P=p,run=r,task_pids=[b[1] for b in parallel]))
            print(f'P={p:2} run={r} serial={ts:.4f}s parallel={tp:.4f}s S={ts/tp:.4f}',flush=True)
    (ROOT/'benchmarks/telemetry.json').write_text(json.dumps(telemetry,indent=2),encoding='utf-8')


if __name__=='__main__':
    mp.freeze_support()
    main()
