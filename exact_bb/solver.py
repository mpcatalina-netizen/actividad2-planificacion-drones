from experiments.model import edge_is_valid, route_cost

DEBUG = True  # Cambia a False para ocultar trazas


def debug(*args):
    if DEBUG:
        print(*args)


def dominates(cost_a, cost_b):
    """
    Devuelve True si cost_a domina a cost_b.
    cost = (distancia, riesgo, bateria)
    """
    return (
        cost_a[0] <= cost_b[0] and
        cost_a[1] <= cost_b[1] and
        cost_a[2] <= cost_b[2] and
        cost_a != cost_b
    )


class ParetoFront:
    def __init__(self):
        self.solutions = []  # lista de (ruta, coste)

    def add(self, route, cost):
        debug(f"[ADD] Intentando añadir ruta {route} con coste {cost}")

        # Si alguna solución existente domina a esta → fuera
        for _, c in self.solutions:
            if dominates(c, cost):
                debug(f"[ADD] Rechazada: {c} domina a {cost}")
                return

        # Eliminamos las que esta domina
        before = len(self.solutions)
        self.solutions = [
            (r, c) for (r, c) in self.solutions
            if not dominates(cost, c)
        ]
        after = len(self.solutions)

        if before != after:
            debug(f"[ADD] Eliminadas {before - after} soluciones dominadas por {cost}")

        self.solutions.append((route[:], cost))
        debug(f"[ADD] Añadida solución: {route} con coste {cost}")


def branch_and_bound(instance, current_route, visited, pareto):
    # Si hemos visitado todos los nodos → cerrar ciclo volviendo al hub
    if len(visited) == len(instance.nodes):
        last = current_route[-1]
        hub = instance.hub_id

        a = instance.nodes[last]
        b = instance.nodes[hub]

        debug(f"[CLOSE] Intentando cerrar ciclo {last} → {hub}")

        if edge_is_valid(a, b, instance.no_fly_zones):
            full_route = current_route + [hub]
            cost = route_cost(full_route, instance)
            debug(f"[CLOSE] Cierre válido. Ruta completa: {full_route}, coste: {cost}")
            pareto.add(full_route, cost)
        else:
            debug(f"[CLOSE] Cierre inválido: arista {last} → {hub} bloqueada")

        return

    last_node_id = current_route[-1]
    last_node = instance.nodes[last_node_id]

    debug(f"\n[EXPAND] Expandiendo desde nodo {last_node_id}. Visitados: {visited}")

    for node_id, node in enumerate(instance.nodes):
        if node_id in visited:
            continue

        # Comprobar arista válida
        valid = edge_is_valid(last_node, node, instance.no_fly_zones)
        debug(f"  - Arista {last_node_id} → {node_id}: {'VÁLIDA' if valid else 'INVÁLIDA'}")

        if not valid:
            continue

        # Coste parcial (para poda)
        partial_route = current_route + [node_id]
        partial_cost = route_cost(partial_route, instance)
        debug(f"    Coste parcial {partial_route}: {partial_cost}")

        # Poda por dominancia
        pruned = False
        for _, c in pareto.solutions:
            if dominates(c, partial_cost):
                debug(f"    PODADA: {c} domina a {partial_cost}")
                pruned = True
                break

        if pruned:
            continue

        visited.add(node_id)
        branch_and_bound(instance, partial_route, visited, pareto)
        visited.remove(node_id)


def solve(instance):
    """
    Algoritmo exacto Branch & Bound multiobjetivo.
    """
    print("[Exact BB] Resolviendo instancia:", instance.name)

    pareto = ParetoFront()

    start = instance.hub_id
    visited = {start}
    branch_and_bound(instance, [start], visited, pareto)

    print(f"\n[Exact BB] Soluciones Pareto encontradas: {len(pareto.solutions)}")

    for route, cost in pareto.solutions:
        print("Ruta:", route, "Coste:", cost)

    return pareto.solutions
