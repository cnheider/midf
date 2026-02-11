import logging

from midf.mi_utilities import clean_admin_id
from midf.model import MIDFAmenity, MIDFSolution
from sync_module.model import (
    LocationType,
    PointOfInterest,
    Room,
    Solution,
)
from sync_module.python_utilities import clean_admin_id_regex
from sync_module.shared import LanguageBundle

__all__ = ["convert_amenities"]


_logger = logging.getLogger(__name__)


def convert_amenities(mi_solution: Solution, midf_solution: MIDFSolution) -> None:
    """

    :param mi_solution:
    :type mi_solution:
    :param midf_solution:
    :type midf_solution:
    :return:
    :rtype:
    """
    if midf_solution.amenities:
        for amenity in midf_solution.amenities:
            amenity: MIDFAmenity

            amenity_name = None
            if amenity.name:
                amenity_name = next(iter(amenity.name.values()))

            if amenity_name is None or amenity_name == "":
                if amenity.alt_name:
                    amenity_name = next(iter(amenity.alt_name.values()))

            if amenity_name is None or amenity_name == "":
                amenity_name = amenity.id

            a = clean_admin_id_regex(amenity.category)

            amenity_category_key = LocationType.compute_key(admin_id=a)
            if mi_solution.location_types.get(amenity_category_key) is None:
                mi_solution.add_location_type(
                    admin_id=a,
                    translations={"en": LanguageBundle(name=amenity.category)},
                )

            for unit in amenity.units:
                ref_unit = mi_solution.rooms.get(
                    Room.compute_key(admin_id=clean_admin_id(unit.id))
                )

                if ref_unit is None:
                    _logger.warning(f"Unit {unit.id} not found in the solution.")
                    continue

                admin_id = clean_admin_id(amenity.id)

                if (
                    mi_solution.points_of_interest.get(
                        PointOfInterest.compute_key(admin_id=admin_id)
                    )
                    is not None
                ):
                    _logger.warning(f"Point of interest {admin_id} already exists.")
                    continue

                mi_solution.add_point_of_interest(
                    admin_id=admin_id,
                    translations={
                        "en": LanguageBundle(
                            name=amenity_name,
                            description=f"{amenity.hours} {amenity.phone} {amenity.website} {amenity.accessibility} "
                            f"{amenity.alt_name} {amenity.correlation_id} {amenity.address}",
                        )
                    },
                    point=amenity.geometry,
                    location_type_key=amenity_category_key,
                    floor_key=ref_unit.floor.key,
                )
