import platform
import psutil
import json
import os
import argparse
from salt import get_student_params

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", required=True)
    args = parser.parse_args()

    # Сбор аппаратной телеметрии
    profile = {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_model": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_threads": psutil.cpu_count(logical=True),
        "base_freq_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown",
        "cache_line_bytes": 64,
        "python_version": platform.python_version()
    }
    
    # Сохранение результатов
    os.makedirs("results", exist_ok=True)
    
    with open("results/host_profile.json", "w") as f:
        json.dump(profile, f, indent=4)
        
    params = get_student_params(args.student_id)
    with open("results/salted_params.json", "w") as f:
        json.dump(params, f, indent=4)
        
    print("M0: Profile and salted params saved.")

if __name__ == "__main__":
    main()