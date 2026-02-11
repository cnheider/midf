import logging
import shapely

from jord.shapely_utilities import clean_shape, dilate
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFOpening
from sync_module.model import Door, LocationType
from sync_module.shared import MIDoorType

_logger = logging.getLogger(__name__)

__all__ = ["convert_openings"]


def convert_openings(level, mi_solution, venue_graph_key, floor_key) -> None:
    """

    :param level:
    :type level:
    :param mi_solution:
    :type mi_solution:
    :param venue_graph_key:
    :type venue_graph_key:
    :param floor_key:
    :type floor_key:
    :return:
    :rtype:
    """
    if level.openings:
        for opening in level.openings:
            opening: MIDFOpening
            opening_name = None
            if opening.name:
                opening_name = next(iter(opening.name.values()))

            if opening_name is None or opening_name == "":
                if opening.alt_name:
                    opening_name = next(iter(opening.alt_name.values()))

            if opening_name is None or opening_name == "":
                opening_name = opening.id

            opening_geom = clean_shape(opening.geometry)

            if False:
                opening_geom = dilate(opening_geom)
                location_type_key = LocationType.compute_key(admin_id=opening.category)
                if mi_solution.location_types.get(location_type_key) is None:
                    location_type_key = mi_solution.add_location_type(
                        admin_id=opening.category, name=opening.category
                    )

                if isinstance(opening_geom, shapely.Polygon):
                    mi_solution.add_area(
                        admin_id=clean_admin_id(opening.id),
                        name=opening_name,
                        polygon=opening_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    _logger.error(f"Ignoring {opening}")
            else:
                a = clean_admin_id(opening.id)

                if mi_solution.doors.get(
                    Door.compute_key(admin_id=a, graph_key=venue_graph_key)
                ):
                    continue

                mi_solution.add_door(
                    admin_id=a,
                    floor_index=level.ordinal,
                    graph_key=venue_graph_key,
                    linestring=opening_geom,
                    door_type=MIDoorType.door,
                )

                # opening.door
