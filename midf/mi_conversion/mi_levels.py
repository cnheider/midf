import logging
from typing import Mapping

from jord.shapely_utilities import clean_shape
from midf.constants import ASSUME_OUTDOOR_IF_MISSING_BUILDING, OUTDOOR_BUILDING_NAME
from midf.mi_conversion.mi_details import convert_details
from midf.mi_conversion.mi_fixtures import convert_fixtures
from midf.mi_conversion.mi_kiosks import convert_kiosks
from midf.mi_conversion.mi_openings import convert_openings
from midf.mi_conversion.mi_sections import (
    convert_sections,
)
from midf.mi_conversion.mi_units import convert_units
from midf.mi_utilities import clean_admin_id, make_mi_building_admin_id_midf
from midf.model import MIDFLevel, MIDFSolution
from sync_module.model import Building, Floor, Solution
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)

__all__ = ["convert_levels"]


def convert_levels(
    anchor_location_type: str,
    found_venue_key: str,
    mi_solution: Solution,
    midf_solution: MIDFSolution,
    occupant_category_mapping: Mapping[str, str],
    venue_graph_key: str,
    venue_key: str,
) -> None:
    for level in midf_solution.levels:
        # level.address TODO: UNUSED ATM
        level: MIDFLevel

        if level.buildings is None or len(level.buildings) == 0:
            if level.outdoor or ASSUME_OUTDOOR_IF_MISSING_BUILDING:
                assert found_venue_key, "Venue key not found"
                c = make_mi_building_admin_id_midf(
                    OUTDOOR_BUILDING_NAME, found_venue_key
                )
                found_building = mi_solution.buildings.get(
                    Building.compute_key(admin_id=clean_admin_id(c))
                )
                if found_building is None:
                    outdoor_building_key = mi_solution.add_building(
                        c,
                        translations={"en": LanguageBundle(name=OUTDOOR_BUILDING_NAME)},
                        polygon=mi_solution.venues.get(venue_key).polygon,
                        venue_key=found_venue_key,
                    )
                    found_building = mi_solution.buildings.get(outdoor_building_key)
            else:
                _logger.error(f"Skipping {level}")
                continue
        else:
            a = make_mi_building_admin_id_midf(
                next(iter(level.buildings)).id, found_venue_key
            )
            found_building = mi_solution.buildings.get(
                Building.compute_key(admin_id=clean_admin_id(a))
            )

        floor_name = None
        if level.name:
            floor_name = next(iter(level.name.values()))

        if floor_name is None or floor_name == "":
            floor_name = level.id

        floor_index = level.ordinal
        while mi_solution.floors.get(
            Floor.compute_key(building_key=found_building.key, floor_index=floor_index)
        ):
            if True:  # TODO: DISABLE WHEN FINISHED TESTING
                floor_index += 100
            else:
                _logger.error(f"Skipping {level}, already exists")
                continue

        floor_key = mi_solution.add_floor(
            building_key=found_building.key,
            translations={"en": LanguageBundle(name=floor_name)},
            polygon=clean_shape(found_building.polygon),
            floor_index=floor_index,
        )

        convert_units(
            anchor_location_type,
            floor_key,
            level,
            mi_solution,
            occupant_category_mapping,
        )

        convert_details(floor_key, level, mi_solution)

        convert_kiosks(floor_key, level, mi_solution)

        convert_sections(floor_key, level, mi_solution)

        convert_fixtures(floor_key, level, mi_solution)

        convert_openings(level, mi_solution, venue_graph_key, floor_key)
