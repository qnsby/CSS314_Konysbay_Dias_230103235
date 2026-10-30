import time
from multiprocessing import Process, Value, Lock

def contended_worker(shared_counter, lock, iterations):
    for _ in range(iterations):
        with lock: # Жесткая конкуренция за блокировку и кэш
            shared_counter.value += 1

def run_contended(p, total_increments=2_000_000):
    increments_per_worker = total_increments // p
    counter = Value('i', 0)
    lock = Lock()
    procs = [Process(target=contended_worker, args=(counter, lock, increments_per_worker)) for _ in range(p)]
    t0 = time.perf_counter()
    for proc in procs: proc.start()
    for proc in procs: proc.join()
    t1 = time.perf_counter()
    assert counter.value == total_increments
    return t1 - t0

if __name__ == "__main__":
    cores = [1, 2, 4]
    runtimes = {p: run_contended(p) for p in cores}
    t1 = runtimes[1]
    
    for p in cores:
        tp = runtimes[p]
        sp = t1 / tp
        e = ((p * tp / t1) - 1.0) / (p - 1.0) if p > 1 else 0
        print(f"Exp B - P={p}: Runtime={tp:.3f}s | Speedup={sp:.2f}x | Karp-Flatt e={e:.3f}")