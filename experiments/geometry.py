def orientation(a, b, c):
    """
    Determina la orientación del triplete (a, b, c).
    > 0: giro antihorario
    < 0: giro horario
    = 0: colineales
    """
    return (b["x"] - a["x"]) * (c["y"] - a["y"]) - (b["y"] - a["y"]) * (c["x"] - a["x"])


def segments_intersect(p1, p2, q1, q2):
    """
    Comprueba si los segmentos p1-p2 y q1-q2 se intersectan.
    """
    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    return o1 * o2 < 0 and o3 * o4 < 0


def segment_intersects_polygon(p1, p2, polygon):
    """
    Comprueba si el segmento p1-p2 intersecta algún lado del polígono.
    """
    n = len(polygon)
    for i in range(n):
        q1 = polygon[i]
        q2 = polygon[(i + 1) % n]

        if segments_intersect(p1, p2, q1, q2):
            return True

    return False

