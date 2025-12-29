import random
import math

from experiments.model import edge_is_valid, route_cost
from geo_heuristic.solver import solve as greedy_init
def route_is_valid(route, instance):
    nodes = instance.nodes
    for i in range(len(route) - 1):
        a = nodes[route[i]]
        b = nodes[route[i + 1]]
        if not edge_is_valid(a, b, instance.no_fly_zones):
            return False
    return True
def generate_neighbor(route):
    # no tocamos ni el primer ni el último (hub)
    i, j = random.sample(range(1, len(route) - 1), 2)
    new_route = route[:]
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route
def scalar_cost(cost):
    # combinación ponderada simple
    return cost[0] + cost[1] + cost[2]
def solve(instance):
    print("[Metaheuristic] Resolviendo instancia:", instance.name)

    # solución inicial (greedy)
    init_solutions = greedy_init(instance)
    if not init_solutions:
        print("[Metaheuristic] No hay solución inicial")
        return []

    current_route, current_cost = init_solutions[0]
    best_route = current_route[:]
    best_cost = current_cost

    T = 100.0
    T_min = 0.1
    alpha = 0.95

    while T > T_min:
        neighbor = generate_neighbor(current_route)

        if not route_is_valid(neighbor, instance):
            T *= alpha
            continue

        neighbor_cost = route_cost(neighbor, instance)

        delta = scalar_cost(neighbor_cost) - scalar_cost(current_cost)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = neighbor
            current_cost = neighbor_cost

            if scalar_cost(current_cost) < scalar_cost(best_cost):
                best_route = current_route[:]
                best_cost = current_cost

        T *= alpha

    print("[Metaheuristic] Mejor ruta:", best_route)
    print("[Metaheuristic] Coste:", best_cost)

    return [(best_route, best_cost)]
