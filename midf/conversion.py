from collections import defaultdict

import logging
import shapely

from jord.shapely_utilities import dilate
from midf.constants import ANCHOR_NAME, OUTDOOR_BUILDING_NAME
from midf.mi_conversion import (
    convert_amenities,
    convert_buildings,
    convert_footprints,
    convert_geofences,
    convert_levels,
    convert_occupant_categories,
    convert_relationships,
    convert_venues,
)
from midf.mi_utilities import make_mi_building_admin_id_midf
from midf.model import MIDFSolution
from sync_module.model import (
    Building,
    FALLBACK_OSM_GRAPH,
    Solution,
)
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)


def to_mi_solution(
    midf_solution: MIDFSolution, solution_name: str = "ChenIMDFImport"
) -> Solution:
    if midf_solution.manifest.generated_by:
        solution_name = midf_solution.manifest.generated_by

    mi_solution = Solution(
        _external_id=f"{solution_name}{midf_solution.manifest.version}",
        _name=solution_name,
        _customer_id="953f7a89334a4013927857ab",
        occupants_enabled=True,
    )

    address_venue_mapping = defaultdict(list)

    venue, venue_key = convert_venues(address_venue_mapping, mi_solution, midf_solution)

    assert venue_key is not None, "No venue was found in the data"

    venue_graph_key = mi_solution.add_graph(
        graph_id=venue_key,
        osm_xml=FALLBACK_OSM_GRAPH,
        boundary=dilate(shapely.Point(0, 0)),
    )

    building_footprint_mapping = defaultdict(list)

    anchor_location_type = mi_solution.add_location_type(
        admin_id=ANCHOR_NAME, translations={"en": LanguageBundle(name=ANCHOR_NAME)}
    )

    occupant_category_mapping = convert_occupant_categories(mi_solution)

    convert_footprints(building_footprint_mapping, midf_solution)

    found_venue_key = convert_buildings(
        address_venue_mapping,
        building_footprint_mapping,
        mi_solution,
        midf_solution,
        venue,
        venue_key,
    )

    convert_levels(
        anchor_location_type,
        found_venue_key,
        mi_solution,
        midf_solution,
        occupant_category_mapping,
        venue_graph_key,
        venue_key,
    )

    convert_amenities(mi_solution, midf_solution)

    convert_geofences(found_venue_key, mi_solution, midf_solution)

    convert_relationships(mi_solution, midf_solution, venue_graph_key)

    solution_locations_union = shapely.convex_hull(
        shapely.unary_union(
            [a.polygon for a in mi_solution.areas]
            + [r.polygon for r in mi_solution.rooms]
            + [r.point for r in mi_solution.points_of_interest]
        )
    )

    if solution_locations_union.is_empty:
        raise Exception("No solution was found in the data")

    blk = make_mi_building_admin_id_midf(OUTDOOR_BUILDING_NAME, found_venue_key)
    if mi_solution.buildings.get(Building.compute_key(admin_id=blk)) is not None:
        mi_solution.update_building(blk, polygon=solution_locations_union)

    mi_solution.update_graph(venue_graph_key, boundary=solution_locations_union)

    mi_solution.update_venue(
        found_venue_key, polygon=solution_locations_union, graph_key=venue_graph_key
    )

    return mi_solution
