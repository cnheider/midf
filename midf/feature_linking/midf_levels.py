from typing import Collection, Dict, List, Mapping

from midf.enums import IMDFFeatureType
from midf.imdf_model import IMDFFeature, IMDFLevel
from midf.model import (
    MIDFBuilding,
    MIDFDetail,
    MIDFFixture,
    MIDFKiosk,
    MIDFLevel,
    MIDFOpening,
    MIDFSection,
    MIDFUnit,
)

__all__ = ["link_levels"]

import logging

_logger = logging.getLogger(__name__)


def link_levels(
    *,
    buildings: Mapping[str, MIDFBuilding],
    found_detail_levels: Collection[str],
    found_fixture_levels: Collection[str],
    found_kiosk_levels: Collection[str],
    found_opening_levels: Collection[str],
    found_section_levels: Collection[str],
    found_unit_levels: Collection[str],
    imdf_dict: Mapping[IMDFFeatureType, Collection[IMDFFeature]],
    details: Dict[str, List[MIDFDetail]],
    fixtures: Dict[str, List[MIDFFixture]],
    kiosks: Dict[str, List[MIDFKiosk]],
    openings: Dict[str, List[MIDFOpening]],
    sections: Dict[str, List[MIDFSection]],
    units: Dict[str, List[MIDFUnit]],
) -> Dict[str, MIDFLevel]:
    """

    :param buildings:
    :type buildings:
    :param found_detail_levels:
    :type found_detail_levels:
    :param found_fixture_levels:
    :type found_fixture_levels:
    :param found_kiosk_levels:
    :type found_kiosk_levels:
    :param found_opening_levels:
    :type found_opening_levels:
    :param found_section_levels:
    :type found_section_levels:
    :param found_unit_levels:
    :type found_unit_levels:
    :param imdf_dict:
    :type imdf_dict:
    :param details:
    :type details:
    :param fixtures:
    :type fixtures:
    :param kiosks:
    :type kiosks:
    :param openings:
    :type openings:
    :param sections:
    :type sections:
    :param units:
    :type units:
    :return:
    :rtype:
    """
    levels = {}
    _logger.error(f"Linking levels from {len(imdf_dict[IMDFFeatureType.level])} levels")

    kiosks_copy = kiosks.copy()
    openings_copy = openings.copy()
    sections_copy = sections.copy()
    units_copy = units.copy()
    fixtures_copy = fixtures.copy()
    details_copy = details.copy()

    for level in imdf_dict[IMDFFeatureType.level]:
        level: IMDFLevel

        building_references = None
        if level.building_ids:
            building_references = []
            for b_id in level.building_ids:
                if b_id in buildings:
                    building_references.append(buildings[b_id])
                else:
                    _logger.error(f"Building {b_id} not found for level {level.id}")

        levels[level.id] = MIDFLevel(
            id=level.id,
            geometry=level.geometry,
            category=level.category,
            outdoor=level.outdoor,
            ordinal=level.ordinal,
            name=level.name,
            short_name=level.short_name,
            restriction=level.restriction,
            # address=addresses[section.address_id], # TODO: INVALID IMDF!
            buildings=building_references,
            sections=(
                sections_copy.pop(level.id)
                if level.id in found_section_levels
                else None
            ),
            kiosks=(
                kiosks_copy.pop(level.id) if level.id in found_kiosk_levels else None
            ),
            fixtures=(
                fixtures_copy.pop(level.id)
                if level.id in found_fixture_levels
                else None
            ),
            openings=(
                openings_copy.pop(level.id)
                if level.id in found_opening_levels
                else None
            ),
            units=(
                units_copy.pop(level.id)
                if level.id in found_unit_levels and level.id in units_copy
                else None
            ),
            details=(
                details_copy.pop(level.id)
                if level.id in found_detail_levels and level.id in details_copy
                else None
            ),
        )
    return levels
