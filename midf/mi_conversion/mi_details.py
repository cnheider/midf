import logging

import shapely

from jord.shapely_utilities import clean_shape, dilate
from midf.constants import DETAIL_LOCATION_TYPE_NAME
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFDetail, MIDFLevel
from sync_module.model import LocationType, Solution
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)

__all__ = ["convert_details"]


def convert_details(floor_key: str, level: MIDFLevel, mi_solution: Solution) -> None:
    """

    :param floor_key:
    :type floor_key:
    :param level:
    :type level:
    :param mi_solution:
    :type mi_solution:
    :return:
    :rtype:
    """
    if level.details:
        for detail in level.details:
            detail: MIDFDetail

            detail_name = detail.id

            detail_geom = dilate(clean_shape(detail.geometry))

            location_type_key = LocationType.compute_key(
                admin_id=DETAIL_LOCATION_TYPE_NAME
            )
            if mi_solution.location_types.get(location_type_key) is None:
                location_type_key = mi_solution.add_location_type(
                    admin_id=DETAIL_LOCATION_TYPE_NAME,
                    translations={"en": LanguageBundle(name=DETAIL_LOCATION_TYPE_NAME)},
                )

            if isinstance(detail_geom, shapely.Polygon):
                mi_solution.add_area(
                    admin_id=clean_admin_id(detail.id),
                    translations={"en": LanguageBundle(name=detail_name)},
                    polygon=detail_geom,
                    floor_key=floor_key,
                    location_type_key=location_type_key,
                )
            else:
                _logger.error(f"Ignoring {detail}")
