import logging

import shapely

from jord.shapely_utilities import clean_shape
from midf.mi_utilities import clean_admin_id
from sync_module.python_utilities import clean_admin_id_regex
from midf.model import MIDFLevel, MIDFSection
from sync_module.model import LocationType, Solution
from sync_module.shared import LanguageBundle

_logger = logging.getLogger(__name__)

__all__ = ["convert_sections"]


def convert_sections(floor_key: str, level: MIDFLevel, mi_solution: Solution) -> None:
    if level.sections:
        for section in level.sections:
            section: MIDFSection

            section_name = None
            if section.name:
                section_name = next(iter(section.name.values()))

            if section_name is None or section_name == "":
                if section.alt_name:
                    section_name = next(iter(section.alt_name.values()))

            if section_name is None or section_name == "":
                section_name = section.id

            section_geom = clean_shape(section.geometry)

            a = clean_admin_id_regex(section.category)
            location_type_key = LocationType.compute_key(admin_id=a)
            if mi_solution.location_types.get(location_type_key) is None:
                location_type_key = mi_solution.add_location_type(
                    admin_id=a,
                    translations={"en": LanguageBundle(name=section.category)},
                )

            if isinstance(section_geom, shapely.Polygon):
                mi_solution.add_area(
                    admin_id=clean_admin_id(section.id),
                    translations={"en": LanguageBundle(name=section_name)},
                    polygon=section_geom,
                    floor_key=floor_key,
                    location_type_key=location_type_key,
                )
            else:
                _logger.error(f"Ignoring {section}")
