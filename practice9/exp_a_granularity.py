import time, math
from multiprocessing import Pool

def collatz_steps(n):
    steps = 0
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

def run_granularity(workers, total_items=1_000_000, chunk_size=1):
    numbers = range(1, total_items + 1)
    t0 = time.perf_counter()
    with Pool(processes=workers) as pool:
        # chunk_size=1 создает 1,000,000 индивидуальных задач (Micro-tasks)
        results = pool.map(collatz_steps, numbers, chunksize=chunk_size)
    return time.perf_counter() - t0, sum(results)

if __name__ == "__main__":
    cores = [1, 2, 4, 8]
    runtimes = {}
    
    for p in cores:
        runtimes[p], _ = run_granularity(p)
    
    t1 = runtimes[1]
    print("\n--- Granularity Karp-Flatt Analysis (Micro-tasks) ---")
    for p in cores:
        tp = runtimes[p]
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0) if p > 1 else 0
        print(f"P={p:2d} | Time={tp:6.3f}s | Speedup={sp:5.2f}x | Karp-Flatt e={e:6.3f}")