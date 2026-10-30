import time
import json
import statistics
import os
import numpy as np

def matmul_naive(A, B, C, M):
    # Наивный подход: i-j-k
    for i in range(M):
        for j in range(M):
            for k in range(M):
                C[i][j] += A[i][k] * B[k][j]

def matmul_interchanged(A, B, C, M):
    # Оптимизированный подход: i-k-j (вынесение A[i][k] в регистр и линейный проход по B)
    for i in range(M):
        for k in range(M):
            a_ik = A[i][k]
            for j in range(M):
                C[i][j] += a_ik * B[k][j]

def main():
    # Загружаем индивидуальные параметры
    with open("results/salted_params.json", "r") as f:
        params = json.load(f)
    
    N = params["N"]
    M = N // 2 # Размер подблока для укладывания в 45-минутный лимит
    print(f"Running dense kernel for sub-block M={M} (N={N})")

    # Инициализация матриц A и B
    np.random.seed(params["seed"])
    A = np.random.rand(M, M).tolist() # Используем стандартные списки Python
    B = np.random.rand(M, M).tolist()
    
    naive_times = []
    interchanged_times = []

    print("Testing Naive (i-j-k)... this may take a minute.")
    for _ in range(3):
        C = np.zeros((M, M)).tolist()
        start = time.perf_counter()
        matmul_naive(A, B, C, M)
        end = time.perf_counter()
        naive_times.append(end - start)

    print("Testing Interchanged (i-k-j)...")
    for _ in range(3):
        C = np.zeros((M, M)).tolist()
        start = time.perf_counter()
        matmul_interchanged(A, B, C, M)
        end = time.perf_counter()
        interchanged_times.append(end - start)

    t_naive = statistics.median(naive_times)
    t_interchanged = statistics.median(interchanged_times)
    speedup = t_naive / t_interchanged if t_interchanged > 0 else 0

    print(f"Naive Median Time: {t_naive:.4f} s")
    print(f"Interchanged Median Time: {t_interchanged:.4f} s")
    print(f"Empirical Speedup (S): {speedup:.2f}x")

    res = {
        "N": N,
        "M": M,
        "naive_time_s": t_naive,
        "interchanged_time_s": t_interchanged,
        "speedup": speedup
    }

    os.makedirs("results", exist_ok=True)
    with open("results/loop_interchange.json", "w") as f:
        json.dump(res, f, indent=4)
        
    print("M1 (Task 1.2): loop_interchange.json generated.")

if __name__ == "__main__":
    main()