import time
import numpy as np
import statistics
import os
import gc

def main():
    buffer_elements = 16_777_216
    data = np.ones(buffer_elements, dtype=np.float64)
    flush_buf = np.ones(4 * 1024 * 1024, dtype=np.float64)
    
    strides = [1, 2, 4, 8, 16, 32, 64, 128]
    results = []

    print("Running Stride Latency Benchmark...")
    
    # Отключаем сборщик мусора для стабильности замеров
    gc.disable()
    
    for s in strides:
        times_ns = []
        elements_touched = buffer_elements // s
        
        for iteration in range(20): # Увеличили количество итераций
            # Сбрасываем кэш
            _ = np.sum(flush_buf)
            
            # Замер
            start = time.perf_counter_ns()
            total = np.sum(data[::s])
            end = time.perf_counter_ns()
            
            if iteration >= 5:
                times_ns.append(end - start)
        
        median_time_ns = statistics.median(times_ns)
        # Убедимся, что время не равно 0, добавив небольшое значение, если медиана нулевая
        if median_time_ns == 0:
            median_time_ns = 1 
            
        latency_per_element = median_time_ns / elements_touched
        results.append(f"{s}\t{int(median_time_ns)}\t{latency_per_element:.4f}\n")
        print(f"Stride: {s:3d} | Median Time: {int(median_time_ns)} ns | Latency/elem: {latency_per_element:.4f} ns")

    gc.enable()

    os.makedirs("results", exist_ok=True)
    with open("results/stride_results.tsv", "w") as f:
        f.write("Stride\tMedianTime_ns\tLatencyPerElement_ns\n")
        f.writelines(results)
    
    print("M1: stride_results.tsv updated.")

if __name__ == "__main__":
    main()