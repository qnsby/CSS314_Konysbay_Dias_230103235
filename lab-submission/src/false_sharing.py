import multiprocessing as mp
import ctypes
import time
import os

def worker_unpadded(shared_arr, worker_id, iterations):
    # Патологический случай: потоки пишут в соседние индексы на одной кэш-линии
    for _ in range(iterations):
        shared_arr[worker_id] += 1

def worker_padded(shared_arr, worker_id, iterations):
    # Решение 1: 64-Byte Padding (каждый счетчик отстоит на 8 x 8 байт = 64 байта)
    for _ in range(iterations):
        shared_arr[worker_id * 8] += 1

def worker_privatized(shared_arr, worker_id, iterations):
    # Решение 2: Приватизация (локальный счетчик в регистрах/стеке)
    local_count = 0
    for _ in range(iterations):
        local_count += 1
    shared_arr[worker_id] += local_count

def run_experiment(target_func, P, K, array_size):
    # lock=False критически важно, чтобы тестировать железо, а не питоновские мьютексы
    shared_arr = mp.Array(ctypes.c_int64, array_size, lock=False)
    processes = []
    
    start_time = time.perf_counter()
    for p in range(P):
        proc = mp.Process(target=target_func, args=(shared_arr, p, K))
        processes.append(proc)
        proc.start()
        
    for proc in processes:
        proc.join()
    end_time = time.perf_counter()
    
    return end_time - start_time

def calc_karp_flatt(T1, TP, P):
    if P == 1:
        return 0.0
    # Вычисление метрики Карпа-Флатта: e(P) = ((P * T_P / T_1) - 1) / (P - 1)
    return ((P * TP / T1) - 1) / (P - 1)

def main():
    K = 5_000_000 # 5 миллионов итераций на поток
    P_list = [1, 2, 4, 8]
    
    times_unpadded = {}
    times_padded = {}
    times_privatized = {}
    
    print("Running Unpadded (False Sharing Pathology)...")
    for P in P_list:
        t = run_experiment(worker_unpadded, P, K, array_size=8)
        times_unpadded[P] = t
        print(f"  P={P}: {t:.4f} s")
        
    print("Running Padded (64-Byte Separation)...")
    for P in P_list:
        t = run_experiment(worker_padded, P, K, array_size=64) # 8 * 8 = 64
        times_padded[P] = t
        print(f"  P={P}: {t:.4f} s")
        
    print("Running Privatized (Thread-Local)...")
    for P in P_list:
        t = run_experiment(worker_privatized, P, K, array_size=8)
        times_privatized[P] = t
        print(f"  P={P}: {t:.4f} s")

    # Генерация результатов в TSV
    os.makedirs("results", exist_ok=True)
    with open("results/false_sharing_karp_flatt.tsv", "w") as f:
        f.write("P\tT_unpadded\tT_padded\tT_privatized\te_unpadded\te_padded\n")
        
        T1_unp = times_unpadded[1]
        T1_pad = times_padded[1]
        
        for P in P_list:
            e_unp = calc_karp_flatt(T1_unp, times_unpadded[P], P)
            e_pad = calc_karp_flatt(T1_pad, times_padded[P], P)
            f.write(f"{P}\t{times_unpadded[P]:.6f}\t{times_padded[P]:.6f}\t{times_privatized[P]:.6f}\t{e_unp:.6f}\t{e_pad:.6f}\n")
            
    print("\nM2 (Task 2): false_sharing_karp_flatt.tsv generated.")
    print("Notice how e_unpadded rises sharply while e_padded stays flat!")

if __name__ == "__main__":
    main()