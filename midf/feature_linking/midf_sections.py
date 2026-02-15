from collections import defaultdict
from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFSection
from midf.model import MIDFSection
from warg.data_structures.mappings import to_dict

__all__ = ["link_sections"]

import logging

_logger = logging.getLogger(__name__)


def link_sections(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, List[MIDFSection]]:
    """

    :param imdf_dict:
    :type imdf_dict:
    :return:
    :rtype:
    """
    sections = defaultdict(list)
    _logger.error(f"Linking {len(imdf_dict[IMDFFeatureType.section])} sections...")
    for section in imdf_dict[IMDFFeatureType.section]:
        section: IMDFSection
        sections[section.level_id].append(
            MIDFSection(
                id=section.id,
                geometry=section.geometry,
                name=section.name,
                alt_name=section.alt_name,
                category=section.category,
                restriction=section.restriction,
                accessibility=section.accessibility,
                display_point=section.display_point,
                correlation_id=section.correlation_id,
                # address=addresses[section.address_id], # TODO: INVALID IMDF!
            )
        )
    # TODO: LINK section PARENTS...
    return to_dict(sections)
