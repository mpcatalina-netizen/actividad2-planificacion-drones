def orientation(a, b, c):
    """
    Determina la orientación del triplete (a, b, c).
    > 0: giro antihorario
    < 0: giro horario
    = 0: colineales
    """
    return (b["x"] - a["x"]) * (c["y"] - a["y"]) - (b["y"] - a["y"]) * (c["x"] - a["x"])


def on_segment(a, b, c):
    """
    Devuelve True si el punto c está sobre el segmento a-b.
    """
    return (
        min(a["x"], b["x"]) <= c["x"] <= max(a["x"], b["x"]) and
        min(a["y"], b["y"]) <= c["y"] <= max(a["y"], b["y"])
    )


def segments_intersect(p1, p2, q1, q2):
    """
    Comprueba si los segmentos p1-p2 y q1-q2 se intersectan.
    Permite tocar vértices y bordes sin considerarlo cruce.
    """
    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    # Caso general: intersección estricta
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True

    # Casos especiales: colinealidad (tocar borde o vértice)
    # NO se consideran intersección prohibida
    if o1 == 0 and on_segment(p1, p2, q1):
        return False
    if o2 == 0 and on_segment(p1, p2, q2):
        return False
    if o3 == 0 and on_segment(q1, q2, p1):
        return False
    if o4 == 0 and on_segment(q1, q2, p2):
        return False

    return False


def segment_intersects_polygon(p1, p2, polygon):
    """
    Devuelve True solo si el segmento p1-p2 cruza el interior del polígono.
    Tocar vértices o bordes NO cuenta como cruce.
    """
    n = len(polygon)
    for i in range(n):
        q1 = polygon[i]
        q2 = polygon[(i + 1) % n]

        if segments_intersect(p1, p2, q1, q2):
            return True

    return False
