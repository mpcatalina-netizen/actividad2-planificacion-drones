from experiments.model import edge_is_valid, route_cost


def solve(instance):
    """
    Heurística geométrica greedy:
    vecino más cercano válido.
    """
    print("[Geo Heuristic] Resolviendo instancia:", instance.name)

    nodes = instance.nodes
    hub = instance.hub_id

    # Ahora nodes es una lista → IDs 0..N-1
    unvisited = set(range(len(nodes)))
    unvisited.remove(hub)

    route = [hub]
    current = hub

    while unvisited:
        best = None
        best_dist = float("inf")

        for nxt in unvisited:
            # Usamos la función edge_is_valid, no un método del instance
            if not edge_is_valid(nodes[current], nodes[nxt], instance.no_fly_zones):
                continue

            d = nodes[current].distance_to(nodes[nxt])
            if d < best_dist:
                best_dist = d
                best = nxt

        if best is None:
            print("[Geo Heuristic] No hay aristas válidas desde", current)
            return []  # sin solución

        route.append(best)
        unvisited.remove(best)
        current = best

    # Volver al hub si es válido
    if edge_is_valid(nodes[current], nodes[hub], instance.no_fly_zones):
        route.append(hub)
    else:
        print("[Geo Heuristic] No se puede volver al hub")
        return []

    # Coste en formato vector
    dist, risk, batt = route_cost(route, instance)

    # Formato estándar: [(ruta, [dist, risk, batt])]
    return [(route, [dist, risk, batt])]
