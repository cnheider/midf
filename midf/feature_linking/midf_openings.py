import logging
from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFOpening
from midf.model import MIDFOpening
from warg.data_structures.mappings import to_dict

__all__ = ["link_openings"]

_logger = logging.getLogger(__name__)


def link_openings(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFOpening]]:
    """

    :param imdf_dict:
    :type imdf_dict:
    :return:
    :rtype:
    """
    openings = defaultdict(list)
    _logger.error(
        f"Linking openings from {len(imdf_dict[IMDFFeatureType.opening])} openings"
    )
    for opening in imdf_dict[IMDFFeatureType.opening]:
        opening: IMDFOpening
        openings[opening.level_id].append(
            MIDFOpening(
                id=opening.id,
                geometry=opening.geometry,
                category=opening.category,
                name=opening.name,
                alt_name=opening.alt_name,
                display_point=opening.display_point,
                door=opening.door,
                accessibility=opening.accessibility,
                access_control=opening.access_control,
            )
        )
    return to_dict(openings)
