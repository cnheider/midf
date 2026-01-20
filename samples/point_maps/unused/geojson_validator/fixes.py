import logging

import shapely

_logger = logging.getLogger(__name__)

__all__ = [
    "fix_unclosed",
    "fix_exterior_not_ccw",
    "fix_interior_not_cw",
    "fix_duplicate_nodes",
]


# Needs manual check: check_less_three_unique_nodes
# Possible but problematic: check_outside_lat_lon_boundaries, check_inner_and_exterior_ring_intersect
def fix_unclosed(geom: shapely.Polygon):
    """Close the geometry by adding the first coordinate at the end if not closed."""
    # TODO Shapely closes anyway
    coords = list(geom.exterior.coords)
    assert len(coords) > 0, f"{geom} has no coordinates"

    if coords[0] != coords[-1]:
        coords.append(coords[0])

    closed_polygon = shapely.Polygon(coords)
    return closed_polygon


def fix_exterior_not_ccw(geom: shapely.Polygon):
    """Reorder exterior ring to be counter-clockwise."""
    if not geom.exterior.is_ccw:
        geom = shapely.Polygon(list(geom.exterior.coords)[::-1])
    return geom


def fix_interior_not_cw(geom: shapely.Polygon):
    """Reorder any interior rings to be clockwise."""
    interiors = []
    exterior = shapely.LinearRing(geom.exterior)
    for interior in geom.interiors:
        if interior.is_ccw:
            interiors.append(shapely.LinearRing(interior.coords[::-1]))
        else:
            interiors.append(shapely.LinearRing(interior))
    return shapely.Polygon(exterior, interiors)


def fix_duplicate_nodes(geom: shapely.Polygon):
    """Remove duplicate nodes from the geometry."""
    return geom.simplify(0)
