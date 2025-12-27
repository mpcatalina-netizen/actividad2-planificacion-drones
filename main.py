import json
import sys

import json
import sys

from experiments.model import load_instance_from_json
from exact_bb.solver import solve as solve_bb
from geo_heuristic.solver import solve as solve_geo
from metaheuristic.solver import solve as solve_meta


def load_instance(path):
    with open(path, "r") as f:
        data = json.load(f)
    return load_instance_from_json(data)


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py instances/inst_test.json")
        sys.exit(1)

    instance = load_instance(sys.argv[1])

    print("Instancia:", instance.name)
    print("Nodos:", len(instance.nodes))
    print("Zonas no-fly:", len(instance.no_fly_zones))
    print("Hub:", instance.get_hub().id)

    solve_bb(instance)
    solve_geo(instance)
    solve_meta(instance)


if __name__ == "__main__":
    main()
