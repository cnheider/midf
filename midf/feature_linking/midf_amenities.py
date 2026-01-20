from collections import defaultdict

import logging
from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAmenity, IMDFFeature
from warg.data_structures.mappings import to_dict

__all__ = ["link_amenities"]

from midf.model import MIDFUnit

from midf.model.solution_level.amenity import MIDFAmenity

_logger = logging.getLogger(__name__)


def link_amenities(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    units: Mapping[str, Collection[MIDFUnit]],
) -> Dict[str, MIDFAmenity]:
    """

    :param imdf_dict:
    :param units:
    :return:
    """
    amenities = defaultdict()

    unit_id_mapping = {unit.id: unit for a in units.values() for unit in a}
    _logger.error(
        f"Linking amenities with {len(imdf_dict[IMDFFeatureType.amenity])} units"
    )
    for amenity in imdf_dict[IMDFFeatureType.amenity]:
        amenity: IMDFAmenity

        mapped_units = []
        if amenity.unit_ids:
            mapped_units = []
            for uid in amenity.unit_ids:
                if uid in unit_id_mapping:
                    mapped_units.append(unit_id_mapping[uid])
                else:
                    _logger.warning(f"Unit {uid} not found for amenity {amenity.id}")

        amenities[amenity.id] = MIDFAmenity(
            id=amenity.id,
            name=amenity.name,
            category=amenity.category,
            hours=amenity.hours,
            phone=amenity.phone,
            website=amenity.website,
            correlation_id=amenity.correlation_id,
            units=mapped_units,
            geometry=amenity.geometry,
        )

    return to_dict(amenities)
