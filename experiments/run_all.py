from experiments.metrics import measure_solver
from experiments.model import load_instance_from_json
from exact_bb.solver import solve as solve_bb
from geo_heuristic.solver import solve as solve_geo
from metaheuristic.solver import solve as solve_meta
from experiments.plots import plot_time_vs_n, plot_cost_vs_n

import json
import os


def load_instance(path):
    with open(path, "r") as f:
        return load_instance_from_json(json.load(f))


def run_instance(instance_path, all_results):
    instance = load_instance(instance_path)
    print("\nInstancia:", instance.name)

    n = len(instance.nodes)

    # Selección dinámica de solvers
    solvers = [
        ("Geo Heuristic", solve_geo),
        ("Metaheuristic", solve_meta)
    ]

    # Exact BB solo para instancias pequeñas
    if n <= 12:
        solvers.insert(0, ("Exact BB", solve_bb))
    else:
        print(f"  (Exact BB desactivado para N = {n}, demasiado grande)")

    for name, solver in solvers:
        t, m, res = measure_solver(solver, instance)

        print(f"{name:15} | Tiempo medio: {t:.4f}s | Memoria: {m:.1f} KB")

        # Extraer coste de forma robusta
        if not res or not res[0]:
            best_cost = None
        else:
            cost_vector = res[0][1]
            if isinstance(cost_vector[0], list):
                cost_vector = cost_vector[0]
            best_cost = sum(cost_vector)

        all_results[name].append((n, t, best_cost))


all_results = {
    "Exact BB": [],
    "Geo Heuristic": [],
    "Metaheuristic": []
}


if __name__ == "__main__":
    for file in os.listdir("instances"):
        if file.endswith(".json"):
            run_instance(os.path.join("instances", file), all_results)

    plot_time_vs_n(all_results)
    plot_cost_vs_n(all_results)

    print("Gráficas guardadas en /plots")
