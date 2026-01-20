import logging

from jord.shapely_utilities import clean_shape
from midf.constants import OUTDOOR_BUILDING_NAME
from midf.mi_utilities import clean_admin_id, make_mi_building_admin_id_midf
from sync_module.python_utilities import clean_admin_id_regex
from midf.model import MIDFGeofence, MIDFSolution
from sync_module.model import Building, LocationType, Solution
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)

__all__ = ["convert_geofences"]


def convert_geofences(
    found_venue_key: str, mi_solution: Solution, midf_solution: MIDFSolution
) -> None:
    if midf_solution.geofences:
        for geofence in midf_solution.geofences:
            geofence: MIDFGeofence

            a = clean_admin_id_regex(geofence.category)

            ltk = LocationType.compute_key(admin_id=a)
            if mi_solution.location_types.get(ltk) is None:
                ltk = mi_solution.add_location_type(
                    admin_id=a,
                    translations={"en": LanguageBundle(name=geofence.category)},
                )

            if geofence.buildings:
                for building in geofence.buildings:
                    ...
            if geofence.levels:
                for level in geofence.levels:
                    ...
            if geofence.parents:
                for parent in geofence.parents:
                    ...

            geofence_name = None
            if geofence.name:
                geofence_name = next(iter(geofence.name.values()))

            if geofence_name is None or geofence_name == "":
                if geofence.alt_name:
                    geofence_name = next(iter(geofence.alt_name.values()))

            if geofence_name is None or geofence_name == "":
                geofence_name = geofence.category

            if geofence_name is None or geofence_name == "":
                geofence_name = geofence.id

            blk = Building.compute_key(
                admin_id=clean_admin_id(
                    make_mi_building_admin_id_midf(
                        OUTDOOR_BUILDING_NAME, found_venue_key
                    )
                )
            )

            floor_key = None
            for floor in mi_solution.floors:
                if floor.building.key == blk:
                    floor_key = floor.key
                    break

            if floor_key is None:  # TODO: FIX, bad assumption
                _logger.error(f"Floor not found for {geofence}")
                floor_key = next(iter(mi_solution.floors)).key

            gid = geofence.id  # + found_venue_key
            mi_solution.add_area(
                admin_id=clean_admin_id(gid),
                translations={"en": LanguageBundle(name=geofence_name)},
                polygon=clean_shape(geofence.geometry),
                floor_key=floor_key,
                location_type_key=ltk,
            )
