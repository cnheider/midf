from collections import defaultdict

from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFOccupant
from midf.model import MIDFOccupant
from warg.data_structures.mappings import to_dict

__all__ = ["link_occupants"]

import logging

_logger = logging.getLogger(__name__)


def link_occupants(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFOccupant]]:
    occupants = defaultdict(list)
    _logger.error(f"Linking {len(imdf_dict[IMDFFeatureType.occupant])} occupants")
    for occupant in imdf_dict[IMDFFeatureType.occupant]:
        occupant: IMDFOccupant
        occupants[occupant.anchor_id].append(
            MIDFOccupant(
                id=occupant.id,
                name=occupant.name,
                category=occupant.category,
                hours=occupant.hours,
                phone=occupant.phone,
                website=occupant.website,
                validity=occupant.validity,
                correlation_id=occupant.correlation_id,
            )
        )
    return to_dict(occupants)
