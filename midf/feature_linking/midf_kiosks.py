from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFKiosk
from midf.model import MIDFAnchor, MIDFKiosk
from warg.data_structures.mappings import to_dict

__all__ = ["link_kiosks"]

import logging

_logger = logging.getLogger(__name__)


def link_kiosks(
    anchor_id_mapping: Mapping[str, MIDFAnchor],
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFKiosk]]:
    """

    :param anchor_id_mapping:
    :type anchor_id_mapping:
    :param imdf_dict:
    :type imdf_dict:
    :return:
    :rtype:
    """
    kiosks = defaultdict(list)
    _logger.error(f"Linking {len(imdf_dict[IMDFFeatureType.kiosk])} kiosks")
    for kiosk in imdf_dict[IMDFFeatureType.kiosk]:
        kiosk: IMDFKiosk
        kiosks[kiosk.level_id].append(
            MIDFKiosk(
                id=kiosk.id,
                geometry=kiosk.geometry,
                name=kiosk.name,
                alt_name=kiosk.alt_name,
                display_point=kiosk.display_point,
                anchor=anchor_id_mapping[kiosk.anchor_id] if kiosk.anchor_id else None,
            )
        )
    return to_dict(kiosks)
