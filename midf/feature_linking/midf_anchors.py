from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFAnchor, IMDFFeature
from midf.model import MIDFAnchor, MIDFOccupant
from warg.data_structures.mappings import to_dict

__all__ = ["link_anchors"]

import logging

_logger = logging.getLogger(__name__)


def link_anchors(
    found_occupant_anchors: Collection[str],
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    occupants: dict[str, List[MIDFOccupant]],
) -> Dict[str, List[MIDFAnchor]]:
    """

    :param found_occupant_anchors:
    :param imdf_dict:
    :param occupants:
    :return:
    """
    anchors = defaultdict(list)
    occupants_copy = occupants.copy()

    _logger.error(f"Linking anchors {len(imdf_dict[IMDFFeatureType.anchor])}")
    for anchor in imdf_dict[IMDFFeatureType.anchor]:
        anchor: IMDFAnchor

        occupants_linked = None
        if anchor.id in found_occupant_anchors:
            if anchor.id in occupants_copy:
                occupants_linked = occupants_copy.pop(anchor.id)
            else:
                _logger.error(
                    f"{anchor.id} not in {found_occupant_anchors}, THIS SHOULD NOT HAPPEN!"
                )

        anchors[anchor.unit_id].append(
            MIDFAnchor(
                id=anchor.id,
                geometry=anchor.geometry,
                # address=addresses[section.address_id], # TODO: INVALID IMDF!
                occupants=occupants_linked,
            )
        )
    return to_dict(anchors)
