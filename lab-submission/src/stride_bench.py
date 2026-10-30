import time
import numpy as np
import statistics
import os

def main():
    # Аллокация плоского массива в физической памяти (16_777_216 элементов)
    buffer_elements = 16_777_216
    data = np.ones(buffer_elements, dtype=np.float64)
    
    strides = [1, 2, 4, 8, 16, 32, 64, 128]
    results = []

    print("Running Stride Latency Benchmark...")
    for s in strides:
        times_ns = []
        elements_touched = buffer_elements // s
        
        # 5 итераций для прогрева кэша, 5 итераций для замера
        for iteration in range(10):
            start = time.perf_counter_ns()
            # Используем numpy.sum с шагом для чистого замера памяти, минимизируя оверхед Python
            total = np.sum(data[::s])
            end = time.perf_counter_ns()
            
            if iteration >= 5:
                times_ns.append(end - start)
        
        median_time_ns = statistics.median(times_ns)
        # Нормализация времени: нс на один элемент
        latency_per_element = median_time_ns / elements_touched
        results.append(f"{s}\t{median_time_ns}\t{latency_per_element:.2f}\n")
        print(f"Stride: {s:3d} | Median Time: {median_time_ns} ns | Latency/elem: {latency_per_element:.2f} ns")

    os.makedirs("results", exist_ok=True)
    with open("results/stride_results.tsv", "w") as f:
        f.write("Stride\tMedianTime_ns\tLatencyPerElement_ns\n")
        f.writelines(results)
    
    print("M1 (Task 1.1): stride_results.tsv generated.")

if __name__ == "__main__":
    main()