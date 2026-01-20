from collections import defaultdict

from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFDetail, IMDFFeature
from midf.model import MIDFDetail
from warg.data_structures.mappings import to_dict

__all__ = ["link_details"]

import logging

_logger = logging.getLogger(__name__)


def link_details(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFDetail]]:
    details = defaultdict(list)
    _logger.error(f"Linking details {len(imdf_dict[IMDFFeatureType.detail])}")
    for detail in imdf_dict[IMDFFeatureType.detail]:
        detail: IMDFDetail
        details[detail.level_id].append(
            MIDFDetail(
                id=detail.id,
                geometry=detail.geometry,
            )
        )
    return to_dict(details)
