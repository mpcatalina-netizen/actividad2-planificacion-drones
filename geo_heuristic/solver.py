from experiments.model import edge_is_valid, route_cost


def solve(instance):
    """
    Heurística geométrica greedy:
    vecino más cercano válido.
    """
    print("[Geo Heuristic] Resolviendo instancia:", instance.name)

    nodes = instance.nodes
    hub = instance.hub_id

    unvisited = set(nodes.keys())
    unvisited.remove(hub)

    route = [hub]
    current = hub

    while unvisited:
        current_node = nodes[current]

        # buscar el nodo válido más cercano
        candidates = []
        for node_id in unvisited:
            node = nodes[node_id]
            if edge_is_valid(current_node, node, instance.no_fly_zones):
                dist = current_node.distance_to(node)
                candidates.append((dist, node_id))

        if not candidates:
            print("[Geo Heuristic] No hay aristas válidas desde", current)
            return []

        _, next_node = min(candidates)
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    # volver al hub
    if edge_is_valid(nodes[current], nodes[hub], instance.no_fly_zones):
        route.append(hub)
    else:
        print("[Geo Heuristic] No se puede volver al hub")
        return []

    cost = route_cost(route, instance)

    print("[Geo Heuristic] Ruta:", route)
    print("[Geo Heuristic] Coste:", cost)

    return [(route, cost)]
