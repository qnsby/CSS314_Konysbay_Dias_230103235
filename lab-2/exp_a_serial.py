import time, math
from multiprocessing import Pool

def heavy_math(n):
    return sum(math.sin(i) * math.cos(i) for i in range(1, n))

def experiment(workers, total_chunks=16, chunk_size=2_000_000):
    t0 = time.perf_counter()
    time.sleep(0.40) # Искусственное узкое место
    with Pool(processes=workers) as pool:
        pool.map(heavy_math, [chunk_size] * total_chunks)
    return time.perf_counter() - t0

if __name__ == '__main__':
    runtimes = {}
    for p in [1, 2, 4]:
        runtimes[p] = experiment(p)
    
    t1 = runtimes[1]
    for p in [1, 2, 4]:
        tp = runtimes[p]
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0) if p > 1 else 0
        print(f"Exp A - P={p}: Runtime={tp:.3f}s | Speedup={sp:.2f}x | e={e:.3f}")