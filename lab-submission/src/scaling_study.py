import multiprocessing as mp
import time
import json
import math
import os
import numpy as np

def stencil_worker(chunk):
    # Простая симуляция 2D-трафарета (stencil update) на куске матрицы
    res = np.copy(chunk)
    # Выполняем несколько итераций для увеличения вычислительной нагрузки
    for _ in range(5):
        # 4 сложения и 1 умножение на элемент
        res[1:-1, 1:-1] = 0.25 * (chunk[:-2, 1:-1] + chunk[2:, 1:-1] + chunk[1:-1, :-2] + chunk[1:-1, 2:])
    return np.sum(res) # Возвращаем сумму для простоты верификации

def main():
    with open("results/salted_params.json", "r") as f:
        params = json.load(f)
    
    N = params["N"]
    P_list = [1, 2, 4, 8] # Тестируем на 1, 2, 4, 8 процессах
    
    print(f"Starting Strong Scaling Study (Fixed size N={N})...")
    strong_times = {}
    data_strong = np.random.rand(N, N)
    
    for P in P_list:
        chunks = np.array_split(data_strong, P)
        start = time.perf_counter()
        with mp.Pool(P) as pool:
            results = pool.map(stencil_worker, chunks)
        end = time.perf_counter()
        strong_times[P] = end - start
        print(f"  P={P}, Time: {strong_times[P]:.4f} s")

    print("\nStarting Weak Scaling Study (Scaled size)...")
    weak_times = {}
    for P in P_list:
        # N_P = ceil(N * sqrt(P)) для сохранения работы O(P)
        Np = math.ceil(N * math.sqrt(P))
        data_weak = np.random.rand(Np, Np)
        chunks = np.array_split(data_weak, P)
        
        start = time.perf_counter()
        with mp.Pool(P) as pool:
            results = pool.map(stencil_worker, chunks)
        end = time.perf_counter()
        weak_times[P] = end - start
        print(f"  P={P} (Np={Np}), Time: {weak_times[P]:.4f} s")

    # Обработка результатов
    os.makedirs("results", exist_ok=True)
    with open("results/scaling_metrics.tsv", "w") as f:
        f.write("P\tT_strong\tSpeedup_strong\tEfficiency\tT_weak\tSpeedup_scaled\n")
        
        T1_s = strong_times[1]
        T1_w = weak_times[1]
        s_fraction = 0.0
        
        for P in P_list:
            # Strong Scaling (Amdahl)
            T_s = strong_times[P]
            S_P = T1_s / T_s if T_s > 0 else 0
            E_P = (S_P / P) * 100
            
            # Расчет последовательной доли 's' по Амдалу (на P > 1)
            if P > 1 and S_P > 0:
                s = ((1/S_P) - (1/P)) / (1 - (1/P))
                s_fraction = max(s_fraction, s) # Берем максимальную оценку
                
            # Weak Scaling (Gustafson)
            T_w = weak_times[P]
            # S_scaled = P * Work(1) * T1 / (Work(P) * Tp) -> Упрощенно: P * (T1 / Tp)
            S_scaled = P * (T1_w / T_w) if T_w > 0 else 0
            
            f.write(f"{P}\t{T_s:.6f}\t{S_P:.6f}\t{E_P:.2f}%\t{T_w:.6f}\t{S_scaled:.6f}\n")

    S_max = 1 / s_fraction if s_fraction > 0 else float('inf')
    print(f"\nEmpirical Serial Fraction (s): {s_fraction:.4f}")
    print(f"Theoretical Max Speedup (Amdahl): {S_max:.2f}x")

    # Task 3.3: Arithmetic Intensity & Roofline
    # Для нашего трафарета: 5 операций с плавающей точкой (4 сложения, 1 умножение) на 1 элемент
    # Чтение/запись: ~16 байт (чтение 8 байт, запись 8 байт). AI = 5 / 16 = 0.3125 FLOPs/Byte
    ai = 5.0 / 16.0
    regime = "Memory-Bandwidth Bound" if ai < 1.0 else "Compute Bound"
    
    roofline_data = {
        "kernel": "2D Stencil",
        "flops_per_element": 5,
        "bytes_per_element": 16,
        "arithmetic_intensity": ai,
        "execution_regime": regime,
        "amdahl_serial_fraction": s_fraction,
        "amdahl_max_speedup": S_max
    }
    
    with open("results/roofline_summary.json", "w") as f:
        json.dump(roofline_data, f, indent=4)
        
    print("M3 (Task 3): scaling_metrics.tsv and roofline_summary.json generated.")

if __name__ == "__main__":
    main()