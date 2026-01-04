from math import sqrt
from experiments.geometry import segment_intersects_polygon



class Node:
    def __init__(self, node_id, x, y, node_type):
        self.id = node_id
        self.x = x
        self.y = y
        self.type = node_type

    def distance_to(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class NoFlyZone:
    def __init__(self, vertices):
        self.vertices = vertices


class DroneInstance:
    def __init__(self, name, nodes, hub_id, no_fly_zones):
        self.name = name
        self.nodes = nodes
        self.hub_id = hub_id
        self.no_fly_zones = no_fly_zones

    def get_hub(self):
        return self.nodes[self.hub_id]


def load_instance_from_json(data):
    nodes = []
    for n in data["nodes"]:
        nodes.append(Node(
            node_id=n["id"],
            x=n["x"],
            y=n["y"],
            node_type=n["type"]
        ))

    zones = []
    for zone in data.get("no_fly_zones", []):
        zones.append(NoFlyZone(zone))

    return DroneInstance(
        name=data["name"],
        nodes=nodes,
        hub_id=data["hub"],
        no_fly_zones=zones
    )



def edge_cost(node_a, node_b):
    """
    Coste multiobjetivo de una arista.
    """
    distance = node_a.distance_to(node_b)
    risk = 0.1 * distance          # modelo simple y justificable
    battery = distance             # consumo proporcional

    return distance, risk, battery


def route_cost(route, instance):
    """
    Coste total de una ruta (lista de IDs de nodos).
    """
    total_dist = 0
    total_risk = 0
    total_battery = 0

    for i in range(len(route) - 1):
        a = instance.nodes[route[i]]
        b = instance.nodes[route[i + 1]]

        d, r, btry = edge_cost(a, b)
        total_dist += d
        total_risk += r
        total_battery += btry

    return total_dist, total_risk, total_battery
 
def edge_is_valid(node_a, node_b, no_fly_zones):
    """
    Devuelve True si el segmento entre node_a y node_b
    NO cruza ninguna zona no-fly.
    """
    p1 = {"x": node_a.x, "y": node_a.y}
    p2 = {"x": node_b.x, "y": node_b.y}

    for zone in no_fly_zones:
        if segment_intersects_polygon(p1, p2, zone.vertices):
            return False

    return True


