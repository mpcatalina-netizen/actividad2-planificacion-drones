import matplotlib.pyplot as plt

def plot_route_comparison(instance, solutions):
    """
    instance: objeto con instance.nodes
    solutions: dict con {"Exact BB": ruta, "Geo": ruta, "Meta": ruta}
    """

    # Dibujar nodos
    xs = [n.x for n in instance.nodes]
    ys = [n.y for n in instance.nodes]


    plt.scatter(xs, ys, c="black")

    # Etiquetas de nodos
    for n in instance.nodes:
        plt.text(n.x + 0.5, n.y + 0.5, str(n.id))

    # Dibujar cada ruta
    colors = {
        "Exact BB": "blue",
        "Geo Heuristic": "orange",
        "Metaheuristic": "green"
    }

    for name, route in solutions.items():
        if route is None:
            continue

        rx = [instance.nodes[i].x for i in route]
        ry = [instance.nodes[i].y for i in route]

        plt.plot(rx, ry, marker='o', label=name, color=colors.get(name, None))

    plt.title(f"Comparación de rutas para {instance.name}")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"plots/routes_{instance.name}.png")
    plt.clf()



def plot_time_vs_n(results):
    """
    results = {
        "Exact BB": [(N, time, cost), ...],
        "Geo Heuristic": [...],
        "Metaheuristic": [...]
    }
    """
    for algo, data in results.items():
        # Filtrar tiempos válidos
        filtered = [(x[0], x[1]) for x in data if x[1] is not None]
        if not filtered:
            continue

        Ns, times = zip(*filtered)
        plt.plot(Ns, times, marker='o', label=algo)

    plt.yscale("log")  # Escala logarítmica para tiempos
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Tiempo medio (s)")
    plt.title("Tiempo de ejecución vs tamaño del problema")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/time_vs_n.png")
    plt.clf()



def plot_cost_vs_n(results):
    for algo, data in results.items():
        # Filtrar costes válidos
        filtered = [(x[0], x[2]) for x in data if x[2] is not None]
        if not filtered:
            continue

        Ns, costs = zip(*filtered)

        # Evitar problemas con valores 0 en escala logarítmica
        costs = [c if c > 0 else 1e-6 for c in costs]

        plt.plot(Ns, costs, marker='o', label=algo)

    plt.yscale("log")  # ⭐ Escala logarítmica para costes
    plt.xlabel("Número de nodos (N)")
    plt.ylabel("Coste total (distancia + riesgo + batería)")
    plt.title("Calidad de la solución vs tamaño del problema")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/cost_vs_n.png")
    plt.clf()
