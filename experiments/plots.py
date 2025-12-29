import matplotlib.pyplot as plt


def plot_time_vs_n(results):
    """
    results = {
        "Exact BB": [(N, time), ...],
        "Geo Heuristic": [...],
        "Metaheuristic": [...]
    }
    """
    for algo, data in results.items():
        Ns = [x[0] for x in data]
        times = [x[1] for x in data]
        plt.plot(Ns, times, marker='o', label=algo)

    plt.yscale("log")
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Tiempo de ejecución vs tamaño del problema")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/time_vs_n.png")
    plt.clf()


def plot_cost_vs_n(results):
    for algo, data in results.items():
        Ns = [x[0] for x in data]
        costs = [x[2] for x in data]
        plt.plot(Ns, costs, marker='o', label=algo)

    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Coste total (distancia + riesgo + batería)")
    plt.title("Calidad de la solución vs tamaño del problema")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/cost_vs_n.png")
    plt.clf()
