import time
import tracemalloc


def measure_solver(solver_func, instance, runs=5):
    times = []
    memories = []
    results = []

    for _ in range(runs):
        tracemalloc.start()
        start = time.perf_counter()

        res = solver_func(instance)

        end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(end - start)
        memories.append(peak / 1024)  # KB
        results.append(res)

    avg_time = sum(times) / len(times)
    avg_memory = sum(memories) / len(memories)

    return avg_time, avg_memory, results
