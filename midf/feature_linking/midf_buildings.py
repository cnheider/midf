import logging
from typing import Collection, Dict, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFBuilding, IMDFFeature
from midf.model import MIDFBuilding

__all__ = ["link_buildings"]

_logger = logging.getLogger(__name__)


def link_buildings(
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
) -> Dict[str, MIDFBuilding]:
    """

    :param imdf_dict:
    :return:
    """
    buildings = {}

    _logger.error(f"IMDF buildings: {imdf_dict[IMDFFeatureType.building]}")

    for building in imdf_dict[IMDFFeatureType.building]:
        building: IMDFBuilding
        buildings[building.id] = MIDFBuilding(
            id=building.id,
            category=building.category,
            name=building.name,
            alt_name=building.alt_name,
            restriction=building.restriction,
            display_point=building.display_point,
            # address=addresses[building.address_id], # TODO: INVALID IMDF!
        )
    return buildings
