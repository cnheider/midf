from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFFootprint
from midf.model import MIDFFootprint
from warg.data_structures.mappings import to_dict

__all__ = ["link_footprints"]

import logging

_logger = logging.getLogger(__name__)


def link_footprints(
    buildings, imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]]
) -> Dict[str, MIDFFootprint]:
    footprints = {}
    _logger.error(
        f"Linking footprints from {len(imdf_dict[IMDFFeatureType.footprint])} footprints"
    )
    for footprint in imdf_dict[IMDFFeatureType.footprint]:
        footprint: IMDFFootprint
        footprints[footprint.id] = MIDFFootprint(
            id=footprint.id,
            geometry=footprint.geometry,
            name=footprint.name,
            category=footprint.category,
            buildings=(
                [buildings[b] for b in footprint.building_ids]
                if footprint.building_ids
                else None
            ),
        )
    return to_dict(footprints)
