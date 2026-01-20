import logging
import shapely
from typing import Mapping

from jord.shapely_utilities import clean_shape
from midf.constants import ANCHOR_NAME
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFLevel, MIDFOccupant, MIDFUnit
from sync_module.model import (
    LocationType,
    Occupant,
    OccupantCategory,
    OccupantTemplate,
    PointOfInterest,
    Room,
    Solution,
)
from sync_module.python_utilities import clean_admin_id_regex
from sync_module.shared import InvalidPolygonError, LanguageBundle, MIOccupantType

_logger = logging.getLogger(__name__)

__all__ = ["convert_units"]


def convert_units(
    anchor_location_type: str,
    floor_key: str,
    level: MIDFLevel,
    mi_solution: Solution,
    occupant_category_mapping: Mapping[str, str],
) -> None:
    if level.units:
        for unit in level.units:
            unit: MIDFUnit

            unit_name = None
            if unit.name:
                unit_name = next(iter(unit.name.values()))

            if unit_name is None or unit_name == "":
                if unit.alt_name:
                    unit_name = next(iter(unit.alt_name.values()))

            if unit_name is None or unit_name == "":
                unit_name = unit.id

            unit_geom = clean_shape(unit.geometry)

            a = clean_admin_id_regex(unit.category)

            location_type_key = LocationType.compute_key(admin_id=a)

            if mi_solution.location_types.get(location_type_key) is None:
                location_type_key = mi_solution.add_location_type(
                    admin_id=a,
                    translations={"en": LanguageBundle(name=unit.category)},
                )

            unit_location_key = clean_admin_id(unit.id)

            if isinstance(unit_geom, shapely.Polygon):
                if False:
                    unit_location_key = mi_solution.add_area(
                        admin_id=unit_location_key,
                        translations={"en": LanguageBundle(name=unit_name)},
                        polygon=unit_geom,
                        floor_key=floor_key,
                        location_type_key=location_type_key,
                    )
                else:
                    if (
                        mi_solution.rooms.get(
                            Room.compute_key(admin_id=unit_location_key)
                        )
                        is not None
                    ):
                        _logger.error(f"Unit {unit.id} already exists. skipping.")
                        continue

                    try:
                        unit_location_key = mi_solution.add_room(
                            admin_id=unit_location_key,
                            translations={"en": LanguageBundle(name=unit_name)},
                            polygon=unit_geom,
                            floor_key=floor_key,
                            location_type_key=location_type_key,
                        )
                    except InvalidPolygonError as e:
                        _logger.error(f"Invalid polygon: {e}")
                        continue
            else:
                _logger.error(f"Ignoring {unit}")
                continue

            if unit.anchors:
                for anchor in unit.anchors:
                    if (
                        mi_solution.occupants.get(
                            Occupant.compute_key(location_key=unit_location_key)
                        )
                        is None
                    ):
                        anchor_key = unit_location_key
                    else:  # Location already has an occupant, add anchor as a point of interest for the occupant to
                        # occupy

                        new_anchor_admin_id = clean_admin_id(anchor.id)
                        mi_solution: Solution

                        while (
                            mi_solution.points_of_interest.get(
                                PointOfInterest.compute_key(
                                    admin_id=new_anchor_admin_id
                                )
                            )
                            is not None
                        ):
                            new_anchor_admin_id += "I"

                        anchor_key = mi_solution.add_point_of_interest(
                            admin_id=new_anchor_admin_id,
                            translations={"en": LanguageBundle(name=ANCHOR_NAME)},
                            point=anchor.geometry,
                            floor_key=floor_key,
                            location_type_key=anchor_location_type,
                        )

                    if anchor.occupants:
                        for occupant in anchor.occupants:
                            occupant: MIDFOccupant

                            occupant_name = None
                            if occupant.name:
                                occupant_name = next(iter(occupant.name.values()))

                            if occupant_name is None or occupant_name == "":
                                occupant_name = occupant.id

                            l = occupant_category_mapping.get(occupant.category)
                            if l is None:
                                _logger.error(
                                    f"Occupant category {occupant.category} not found."
                                )
                                if False:  # FAIL HERE! continue to next occupant
                                    _logger.error(
                                        f"Occupant category {occupant.category} not found."
                                    )
                                    continue
                                else:
                                    aa = mi_solution.occupant_categories.get(
                                        OccupantCategory.compute_key(
                                            name=occupant.category
                                        )
                                    )
                                    if aa is None:
                                        l = mi_solution.add_occupant_category(
                                            occupant.category
                                        )
                                    else:
                                        l = aa.key

                            a = OccupantTemplate.compute_key(
                                name=occupant_name,
                                occupant_category_key=l,
                            )
                            if mi_solution.occupant_templates.get(a) is None:
                                occupant_template_key = mi_solution.add_occupant_template(
                                    name=occupant_name,
                                    occupant_type=MIOccupantType.occupant,
                                    occupant_category_key=l,
                                    description=f"{occupant.hours} {occupant.phone} {occupant.website}",
                                    # business_hours=occupant.hours, # TODO: CONVERT?
                                    # contact=occupant.phone + occupant.website,
                                )
                            else:
                                occupant_template_key = a

                            if (
                                mi_solution.occupants.get(
                                    Occupant.compute_key(location_key=anchor_key)
                                )
                                is not None
                            ):
                                _logger.error(
                                    f"Occupant {occupant.id} already exists. skipping."
                                )
                                continue

                            mi_solution.add_occupant(
                                location_key=anchor_key,
                                occupant_template_key=occupant_template_key,
                            )
