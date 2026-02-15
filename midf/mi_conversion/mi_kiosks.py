import logging

import shapely

from jord.shapely_utilities import clean_shape
from midf.constants import KIOSK_LOCATION_TYPE_NAME
from midf.mi_utilities import clean_admin_id
from midf.model import MIDFKiosk, MIDFLevel
from sync_module.model import LocationType, Solution
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)

__all__ = ["convert_kiosks"]


def convert_kiosks(floor_key: str, level: MIDFLevel, mi_solution: Solution) -> None:
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
    if level.kiosks:
        for kiosk in level.kiosks:
            kiosk: MIDFKiosk

            kiosk_name = None
            if kiosk.name:
                kiosk_name = next(iter(kiosk.name.values()))

            if kiosk_name is None or kiosk_name == "":
                if kiosk.alt_name:
                    kiosk_name = next(iter(kiosk.alt_name.values()))

            if kiosk_name is None or kiosk_name == "":
                kiosk_name = kiosk.id

            kiosk_geom = clean_shape(kiosk.geometry)

            location_type_key = LocationType.compute_key(
                admin_id=KIOSK_LOCATION_TYPE_NAME
            )
            if mi_solution.location_types.get(location_type_key) is None:
                location_type_key = mi_solution.add_location_type(
                    admin_id=KIOSK_LOCATION_TYPE_NAME,
                    translations={"en": LanguageBundle(name=KIOSK_LOCATION_TYPE_NAME)},
                )

            if isinstance(kiosk_geom, shapely.Polygon):
                mi_solution.add_area(
                    admin_id=clean_admin_id(kiosk.id),
                    translations={"en": LanguageBundle(name=kiosk_name)},
                    polygon=kiosk_geom,
                    floor_key=floor_key,
                    location_type_key=location_type_key,
                )
            else:
                _logger.error(f"Ignoring {kiosk}")
